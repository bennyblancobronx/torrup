"""Metadata extraction utilities (exiftool, ffmpeg)."""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from src.utils.core import human_size, now_iso, validate_path_for_subprocess

logger = logging.getLogger(__name__)

# Higher priority formats first (lower number = preferred).
AUDIO_PRIORITY = {".flac": 0, ".wav": 1, ".m4a": 2, ".mp3": 3, ".ogg": 4, ".opus": 5}

_SKIP_SUFFIXES = {".tmp", ".bak"}


def write_xml_metadata(
    release_name: str,
    media_type: str,
    path: Path,
    size_bytes: int,
    torrent_path: Path,
    nfo_path: Path,
    tags: str,
    out_dir: Path,
    metadata: dict | None = None,
    thumb_path: Path | None = None,
) -> Path:
    """Write XML sidecar file with upload metadata."""
    xml_path = out_dir / f"{release_name}.xml"
    metadata = metadata or {}

    root = ET.Element("tlt")
    ET.SubElement(root, "release_name").text = release_name
    ET.SubElement(root, "media_type").text = media_type
    ET.SubElement(root, "path").text = str(path)
    ET.SubElement(root, "size_bytes").text = str(size_bytes)
    ET.SubElement(root, "size_human").text = human_size(size_bytes)
    ET.SubElement(root, "torrent_path").text = str(torrent_path)
    ET.SubElement(root, "nfo_path").text = str(nfo_path)
    if thumb_path:
        ET.SubElement(root, "thumb_path").text = str(thumb_path)
    ET.SubElement(root, "tags").text = tags
    ET.SubElement(root, "created_at").text = now_iso()

    # Add extracted metadata
    if metadata:
        meta_elem = ET.SubElement(root, "metadata")
        for key, value in metadata.items():
            if value:
                ET.SubElement(meta_elem, key).text = str(value)

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    return xml_path


def extract_metadata(path: Path, media_type: str = "movies") -> dict:
    """Extract metadata from files using exiftool and NFO parsing.

    Returns dict with standardized keys based on media type:
    - movies/tv: title, year, description, imdb, tvmazeid, tvmazetype
    - music: artist, album, track, year, genre, format, bitrate, channels, source
    - books: title, author, publisher, year
    """
    if not shutil.which("exiftool"):
        logger.warning("exiftool not installed -- metadata extraction disabled")
        return {}

    target = _find_primary_file(path, media_type)
    result = {}

    # 1. Try NFO parsing first (often more reliable for IDs)
    if path.is_dir() or path.suffix.lower() == ".nfo":
        result.update(_extract_ids_from_nfos(path))

    if not target or not validate_path_for_subprocess(target):
        return result

    try:
        # Single exiftool call -- request all fields we need (including audio).
        exif_result = subprocess.run(
            ["exiftool", "-json", "-n", str(target)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if exif_result.returncode == 0:
            data = json.loads(exif_result.stdout)
            if data:
                raw = data[0]
                result.update(_normalize_metadata(raw, media_type))

                # Derive audio properties from the same exiftool output.
                if media_type == "music":
                    result.update(_audio_props_from_exif(raw))

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, json.JSONDecodeError):
        pass

    return {k: v for k, v in result.items() if v}


def _audio_props_from_exif(raw: dict) -> dict:
    """Derive audio properties from an already-loaded exiftool dict.

    Avoids a second subprocess call -- reuses the full JSON output that
    extract_metadata() already fetched.
    """
    props: dict[str, str] = {
        "format": "MP3",
        "bitrate": "320",
        "channels": "2.0",
        "source": "WEB",  # Default assumption
    }

    try:
        ft = str(raw.get("FileType", "")).upper()
        props["format"] = ft if ft in ("FLAC", "MP3", "OGG", "OPUS", "M4A", "WAV") else "MP3"

        # Bitrate / quality
        if props["format"] == "FLAC":
            bits = raw.get("BitsPerSample", 16)
            props["bitrate"] = "24bit" if int(bits) > 16 else "16bit"
        else:
            br = raw.get("AudioBitrate", "320000")
            if isinstance(br, str):
                br = "".join(filter(str.isdigit, br))
            br_val = int(br) if br else 320000

            if br_val >= 320000:
                props["bitrate"] = "320"
            elif br_val >= 256000:
                props["bitrate"] = "V0"
            else:
                props["bitrate"] = "V2"

        # Channels
        ch = raw.get("Channels", 2)
        props["channels"] = "2.0" if int(ch) == 2 else "1.0"
    except (ValueError, TypeError):
        pass

    return props

def _extract_ids_from_nfos(path: Path) -> dict:
    """Scan directory for .nfo files and extract IMDB/TVMaze IDs."""
    ids = {}
    nfo_files = []
    if path.is_file() and path.suffix.lower() == ".nfo":
        nfo_files.append(path)
    elif path.is_dir():
        nfo_files.extend(list(path.glob("*.nfo")) + list(path.glob("*.NFO")))

    imdb_pattern = re.compile(r"tt\d{7,9}")
    tvmaze_pattern = re.compile(r"tvmaze\.com/shows/(\d+)")

    for nfo in nfo_files:
        try:
            content = nfo.read_text(errors="ignore")
            # IMDB
            imdb_match = imdb_pattern.search(content)
            if imdb_match and not ids.get("imdb"):
                ids["imdb"] = imdb_match.group(0)
            
            # TVMaze
            tvmaze_match = tvmaze_pattern.search(content)
            if tvmaze_match and not ids.get("tvmazeid"):
                ids["tvmazeid"] = tvmaze_match.group(1)
        except Exception:
            continue
    return ids


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


def _normalize_metadata(raw: dict, media_type: str) -> dict:
    """Normalize exiftool output to standard keys."""
    result = {}

    if media_type in ("movies", "tv"):
        result["title"] = raw.get("Title") or raw.get("MovieName") or ""
        result["year"] = raw.get("Year") or raw.get("ContentCreateDate", "")[:4] if raw.get("ContentCreateDate") else ""
        result["description"] = raw.get("Description") or raw.get("Comment") or ""
        
        # ID Extraction from tags
        result["imdb"] = raw.get("IMDB") or raw.get("IMDB_ID") or ""
        result["tvmazeid"] = raw.get("TVMAZE_ID") or raw.get("TVMazeID") or ""
        
        # TV specific
        if media_type == "tv":
            result["show"] = raw.get("TVShow") or raw.get("Album") or ""
            result["season"] = raw.get("TVSeason") or raw.get("SeasonNumber") or ""
            result["episode"] = raw.get("TVEpisode") or raw.get("EpisodeNumber") or ""

    elif media_type == "music":
        result["artist"] = raw.get("Artist") or raw.get("AlbumArtist") or ""
        result["album"] = raw.get("Album") or ""
        result["track"] = raw.get("Title") or raw.get("Track") or ""
        result["year"] = str(raw.get("Year") or "")
        result["genre"] = raw.get("Genre") or ""
        result["track_number"] = raw.get("TrackNumber") or ""

    elif media_type == "books":
        result["title"] = raw.get("Title") or ""
        result["author"] = raw.get("Author") or raw.get("Creator") or ""
        result["publisher"] = raw.get("Publisher") or ""
        result["year"] = str(raw.get("CreateDate", ""))[:4] if raw.get("CreateDate") else ""
        result["isbn"] = raw.get("ISBN") or ""

    # Clean empty strings
    return {k: v for k, v in result.items() if v}


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
