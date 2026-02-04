"""Metadata extraction utilities (exiftool, ffmpeg)."""

from __future__ import annotations

import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from src.utils.core import human_size, now_iso, validate_path_for_subprocess


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
    """Extract metadata from files using exiftool.

    Returns dict with standardized keys based on media type:
    - movies/tv: title, year, description
    - music: artist, album, track, year, genre
    - books: title, author, publisher, year
    """
    target = _find_primary_file(path, media_type)
    if not target or not validate_path_for_subprocess(target):
        return {}

    try:
        result = subprocess.run(
            ["exiftool", "-json", "-n", str(target)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return {}

        data = json.loads(result.stdout)
        if not data:
            return {}

        raw = data[0]
        return _normalize_metadata(raw, media_type)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, json.JSONDecodeError):
        return {}


def _find_primary_file(path: Path, media_type: str) -> Path | None:
    """Find the primary file to extract metadata from."""
    if path.is_file():
        return path

    extensions = {
        "movies": [".mkv", ".mp4", ".avi", ".m4v"],
        "tv": [".mkv", ".mp4", ".avi", ".m4v"],
        "music": [".flac", ".mp3", ".m4a", ".ogg", ".opus"],
        "books": [".epub", ".pdf", ".mobi", ".azw3"],
    }

    exts = extensions.get(media_type, extensions["movies"])
    for f in path.rglob("*"):
        if f.suffix.lower() in exts:
            return f
    return None


def _normalize_metadata(raw: dict, media_type: str) -> dict:
    """Normalize exiftool output to standard keys."""
    result = {}

    if media_type in ("movies", "tv"):
        result["title"] = raw.get("Title") or raw.get("MovieName") or ""
        result["year"] = raw.get("Year") or raw.get("ContentCreateDate", "")[:4] if raw.get("ContentCreateDate") else ""
        result["description"] = raw.get("Description") or raw.get("Comment") or ""
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


def extract_all_album_art(path: Path, out_dir: Path, release_name: str) -> list[Path]:
    """Extract album art from all audio files in a directory.

    Returns list of extracted image paths.
    """
    if path.is_file():
        result = _extract_album_art(path, out_dir / f"{release_name}.jpg")
        return [result] if result else []

    extracted = []
    audio_exts = {".flac", ".mp3", ".m4a", ".ogg", ".opus"}
    seen_albums = set()

    for f in sorted(path.rglob("*")):
        if f.suffix.lower() not in audio_exts:
            continue

        # Use parent folder as album identifier to avoid duplicates
        album_key = str(f.parent)
        if album_key in seen_albums:
            continue

        thumb_name = f"{release_name}_{len(extracted) + 1}.jpg"
        result = _extract_album_art(f, out_dir / thumb_name)
        if result:
            extracted.append(result)
            seen_albums.add(album_key)

    return extracted
