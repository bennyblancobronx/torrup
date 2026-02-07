"""Media helpers: thumbnail extraction, ffprobe, lyrics, album art."""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path

from src.utils.core import human_size, validate_path_for_subprocess

logger = logging.getLogger(__name__)

# Higher priority formats first (lower number = preferred).
AUDIO_PRIORITY = {".flac": 0, ".wav": 1, ".m4a": 2, ".mp3": 3, ".ogg": 4, ".opus": 5}

_SKIP_SUFFIXES = {".tmp", ".bak"}


def _find_primary_file(path: Path, media_type: str) -> Path | None:
    """Find the primary file to extract metadata from.

    For music, files are sorted by format quality (FLAC > WAV > M4A > MP3 > OGG > OPUS).
    Hidden files (starting with '.') and temp files (.tmp, .bak) are always skipped.
    """
    if path.is_file():
        return path

    extensions = {
        "movies": {".mkv", ".mp4", ".avi", ".m4v"},
        "tv": {".mkv", ".mp4", ".avi", ".m4v"},
        "music": set(AUDIO_PRIORITY.keys()),
        "books": {".epub", ".pdf", ".mobi", ".azw3"},
    }

    exts = extensions.get(media_type, extensions["movies"])

    if media_type == "music":
        # Collect all valid audio files, then pick the highest quality format.
        audio_files = [
            f
            for f in path.rglob("*")
            if f.is_file()
            and not f.name.startswith(".")
            and f.suffix.lower() not in _SKIP_SUFFIXES
            and f.suffix.lower() in exts
        ]
        if not audio_files:
            return None
        audio_files.sort(key=lambda f: AUDIO_PRIORITY.get(f.suffix.lower(), 99))
        return audio_files[0]

    # Non-music: return first matching file (skip hidden/temp).
    for f in path.rglob("*"):
        if (
            f.is_file()
            and not f.name.startswith(".")
            and f.suffix.lower() not in _SKIP_SUFFIXES
            and f.suffix.lower() in exts
        ):
            return f
    return None


def extract_thumbnail(
    path: Path,
    out_dir: Path,
    release_name: str,
    media_type: str = "movies",
) -> Path | None:
    """Extract thumbnail from video or album art from audio.

    Returns path to extracted image or None if extraction failed.
    """
    target = _find_primary_file(path, media_type)
    if not target or not validate_path_for_subprocess(target):
        return None

    thumb_path = out_dir / f"{release_name}.jpg"

    if media_type in ("movies", "tv"):
        return _extract_video_thumbnail(target, thumb_path)
    elif media_type == "music":
        return _extract_album_art(target, thumb_path)

    return None


def _extract_video_thumbnail(video_path: Path, out_path: Path) -> Path | None:
    """Extract a frame from video at ~10% duration."""
    try:
        # Get duration first
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            str(video_path),
        ]
        result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)

        seek_time = "00:00:30"  # Default to 30 seconds
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                duration = float(data.get("format", {}).get("duration", 300))
                seek_seconds = int(duration * 0.1)  # 10% into video
                seek_time = f"{seek_seconds // 3600:02d}:{(seek_seconds % 3600) // 60:02d}:{seek_seconds % 60:02d}"
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

        # Extract frame
        cmd = [
            "ffmpeg", "-y",
            "-ss", seek_time,
            "-i", str(video_path),
            "-vframes", "1",
            "-vf", "scale=320:-1",
            "-q:v", "2",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)

        if out_path.exists() and out_path.stat().st_size > 0:
            return out_path
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        pass

    return None


def _extract_album_art(audio_path: Path, out_path: Path) -> Path | None:
    """Extract embedded album artwork from audio file."""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(audio_path),
            "-an",
            "-vcodec", "mjpeg",
            "-vframes", "1",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)

        if out_path.exists() and out_path.stat().st_size > 0:
            return out_path
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
        pass

    return None


def _album_art_from_exif(raw: dict) -> dict | None:
    """Extract album art summary from exiftool output (no binary data)."""
    pic_type = raw.get("PictureType") or raw.get("CoverArt") or raw.get("CoverArtType")
    mime = raw.get("MIMEType") or raw.get("PictureMIMEType")
    size = raw.get("PictureLength") or raw.get("CoverArtLength") or raw.get("ImageSize")
    if not (pic_type or mime or size):
        return None

    info = {}
    if mime:
        info["format"] = mime
    elif pic_type:
        info["format"] = str(pic_type)

    if size:
        if isinstance(size, (int, float)):
            info["size"] = human_size(int(size))
        else:
            info["size"] = str(size)

    return info or None


def _find_local_lyrics(path: Path) -> list[dict]:
    """Find local lyrics files (.lrc/.txt) alongside audio files."""
    base = path.parent if path.is_file() else path
    if not base.exists():
        return []

    lyrics_files = list(base.rglob("*.lrc")) + list(base.rglob("*.LRC"))
    lyrics_files += list(base.rglob("*.txt")) + list(base.rglob("*.TXT"))

    # Build a set of audio track stems to avoid unrelated .txt files.
    audio_stems = set()
    for f in base.rglob("*"):
        if f.is_file() and f.suffix.lower() in AUDIO_PRIORITY:
            audio_stems.add(f.stem)

    entries: list[dict] = []
    for lf in lyrics_files:
        if not lf.is_file():
            continue
        name = lf.stem
        # Filter to likely lyrics files.
        if "lyric" not in name.lower() and name not in audio_stems:
            continue
        lang = None
        if "." in name:
            base_name, maybe_lang = name.rsplit(".", 1)
            if len(maybe_lang) in (2, 3):
                name = base_name
                lang = maybe_lang
        entries.append({"track": name, "lang": lang})

    return entries


def _audio_props_from_ffprobe(path: Path) -> dict:
    """Extract audio stream properties via ffprobe (ffmpeg)."""
    if not shutil.which("ffprobe"):
        return {}

    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries",
            "stream=codec_name,channels,channel_layout,sample_rate,bit_rate,bits_per_sample,bits_per_raw_sample",
            "-of", "json",
            str(path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {}
        data = json.loads(result.stdout)
        stream = (data.get("streams") or [{}])[0]

        props: dict[str, str] = {}
        codec = str(stream.get("codec_name", "")).upper()
        if codec:
            if codec == "FLAC":
                props["format"] = "FLAC"
            elif codec == "MP3":
                props["format"] = "MP3"
            elif codec in ("AAC", "ALAC", "M4A"):
                props["format"] = "M4A"
            elif codec == "OPUS":
                props["format"] = "OPUS"
            elif codec == "VORBIS":
                props["format"] = "OGG"
            else:
                props["format"] = codec

        sr = stream.get("sample_rate")
        if sr:
            try:
                sr_val = float(sr)
                props["sample_rate"] = f"{sr_val / 1000:.1f} kHz" if sr_val >= 1000 else f"{sr_val:.0f} Hz"
            except (ValueError, TypeError):
                pass

        bits = stream.get("bits_per_raw_sample") or stream.get("bits_per_sample")
        if bits:
            try:
                props["bit_depth"] = str(int(bits))
            except (ValueError, TypeError):
                pass

        ch = stream.get("channels")
        if ch:
            try:
                ch_val = int(ch)
                if ch_val == 1:
                    props["channels"] = "1.0"
                elif ch_val == 2:
                    props["channels"] = "2.0"
                elif ch_val == 6:
                    props["channels"] = "5.1"
                elif ch_val == 8:
                    props["channels"] = "7.1"
                else:
                    props["channels"] = str(ch_val)
            except (ValueError, TypeError):
                pass

        br = stream.get("bit_rate")
        if br:
            try:
                br_val = int(br)
                props["bitrate_kbps"] = f"{int(br_val / 1000)} kbps"
            except (ValueError, TypeError):
                pass

        return props
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, json.JSONDecodeError):
        return {}


def _has_embedded_lyrics(raw: dict) -> bool:
    """Check for embedded lyrics tags in exiftool output."""
    lyric_keys = (
        "Lyrics",
        "Lyric",
        "UnsynchronizedLyrics",
        "SynchronizedLyrics",
        "USLT",
        "SYLT",
    )
    for key in lyric_keys:
        val = raw.get(key)
        if val:
            return True
    return False
