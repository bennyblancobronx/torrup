"""NFO generation utilities."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

from src.config import NFO_TEMPLATES
from src.utils.core import get_folder_size, human_size, validate_path_for_subprocess


def generate_nfo(
    path: Path,
    release_name: str,
    out_dir: Path,
    media_type: str = "movies",
    release_group: str = "Torrup",
    metadata: dict | None = None,
) -> Path:
    """Generate NFO file using template and mediainfo."""
    nfo_path = out_dir / f"{release_name}.nfo"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata = metadata or {}

    # Get mediainfo for audio/video files
    media_extensions = {".flac", ".mp3", ".m4a", ".mkv", ".mp4", ".avi", ".m4v"}
    media_file = None
    for f in path.rglob("*"):
        if f.suffix.lower() in media_extensions:
            media_file = f
            break

    mediainfo = ""
    if media_file and validate_path_for_subprocess(media_file):
        try:
            result = subprocess.run(
                ["mediainfo", str(media_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            mediainfo = "\n".join(
                line
                for line in result.stdout.split("\n")
                if not line.strip().startswith("Complete name")
            )
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
            mediainfo = "  MediaInfo not available"

    # Count files and calculate size for books/magazines
    file_count = sum(1 for f in path.rglob("*") if f.is_file()) if path.is_dir() else 1
    size_bytes = get_folder_size(path) if path.is_dir() else path.stat().st_size

    # Extract info from release name for template (use metadata if available)
    source = _extract_source(release_name)
    resolution = _extract_resolution(release_name)
    file_format = _extract_format(release_name, path)

    # Build metadata section if we have extracted data
    metadata_section = _format_metadata_section(metadata, media_type)

    # Get template
    template = NFO_TEMPLATES.get(media_type, NFO_TEMPLATES["movies"])

    # Fill template
    nfo_content = template.format(
        release_name=release_name,
        release_group=release_group,
        source=source,
        resolution=resolution,
        format=file_format,
        mediainfo=mediainfo.strip() if mediainfo else "  No media info available",
        file_count=file_count,
        size=human_size(size_bytes),
        timestamp=timestamp,
    )

    # Insert metadata section before mediainfo if available
    if metadata_section:
        nfo_content = nfo_content.replace(
            "MEDIA INFO",
            f"METADATA\n{'-' * 80}\n{metadata_section}\n{'-' * 80}\n{'MEDIA INFO':^80}"
        )

    nfo_path.write_text(nfo_content)
    return nfo_path


def _format_metadata_section(metadata: dict, media_type: str) -> str:
    """Format extracted metadata for NFO display."""
    if not metadata:
        return ""

    lines = []
    if media_type in ("movies", "tv"):
        if metadata.get("title"):
            lines.append(f"  Title          : {metadata['title']}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("description"):
            desc = metadata["description"][:100] + "..." if len(metadata.get("description", "")) > 100 else metadata.get("description", "")
            lines.append(f"  Description    : {desc}")
        if media_type == "tv":
            if metadata.get("show"):
                lines.append(f"  Show           : {metadata['show']}")
            if metadata.get("season"):
                lines.append(f"  Season         : {metadata['season']}")
            if metadata.get("episode"):
                lines.append(f"  Episode        : {metadata['episode']}")

    elif media_type == "music":
        if metadata.get("artist"):
            lines.append(f"  Artist         : {metadata['artist']}")
        if metadata.get("album"):
            lines.append(f"  Album          : {metadata['album']}")
        if metadata.get("track"):
            lines.append(f"  Track          : {metadata['track']}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("genre"):
            lines.append(f"  Genre          : {metadata['genre']}")

    elif media_type in ("books", "magazines"):
        if metadata.get("title"):
            lines.append(f"  Title          : {metadata['title']}")
        if metadata.get("author"):
            lines.append(f"  Author         : {metadata['author']}")
        if metadata.get("publisher"):
            lines.append(f"  Publisher      : {metadata['publisher']}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("isbn"):
            lines.append(f"  ISBN           : {metadata['isbn']}")

    return "\n".join(lines)


def _extract_source(name: str) -> str:
    """Extract source type from release name."""
    sources = [
        "BluRay", "Bluray", "REMUX", "WEB-DL", "WEBDL", "WEBRip", "WEBRIP",
        "HDTV", "DVDRip", "DVD-R", "DVDR", "BDRip", "HDRip", "CAM", "TS", "TC",
        "CD", "WEB", "Vinyl", "SACD",
    ]
    name_upper = name.upper()
    for src in sources:
        if src.upper() in name_upper:
            return src
    return "Unknown"


def _extract_resolution(name: str) -> str:
    """Extract resolution from release name."""
    resolutions = ["2160p", "4K", "1080p", "1080i", "720p", "576p", "480p", "SD"]
    name_upper = name.upper()
    for res in resolutions:
        if res.upper() in name_upper:
            return res
    return "Unknown"


def _extract_format(name: str, path: Path) -> str:
    """Extract format from release name or file extension."""
    formats = ["FLAC", "MP3", "AAC", "OGG", "EPUB", "PDF", "MOBI", "AZW3", "CBR", "CBZ"]
    name_upper = name.upper()
    for fmt in formats:
        if fmt in name_upper:
            return fmt
    # Try file extension
    if path.is_file():
        ext = path.suffix.upper().lstrip(".")
        if ext in formats:
            return ext
    # Check first file in directory
    if path.is_dir():
        for f in path.rglob("*"):
            if f.is_file():
                ext = f.suffix.upper().lstrip(".")
                if ext in ["FLAC", "MP3", "EPUB", "PDF", "MOBI", "CBR", "CBZ"]:
                    return ext
                break
    return "Unknown"
