"""Core utility functions for file operations."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    """Return current UTC time in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


def human_size(size: int) -> str:
    """Convert bytes to human-readable size string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def get_folder_size(path: Path, max_files: int = 50000) -> int:
    """Calculate total size of all files in a directory.

    Args:
        path: Directory path to calculate size for
        max_files: Maximum number of files to process (default 50000)

    Returns:
        Total size in bytes

    Raises:
        ValueError: If directory contains more than max_files
    """
    total = 0
    count = 0
    for f in path.rglob("*"):
        if f.is_file():
            count += 1
            if count > max_files:
                raise ValueError(f"Directory contains more than {max_files} files")
            total += f.stat().st_size
    return total


def sanitize_release_name(name: str) -> str:
    """Clean up release name for torrent naming. Prevent path traversal."""
    if not name:
        return "unnamed"
    # Remove any path components
    name = name.replace('/', '.').replace('\\', '.').replace('..', '.')
    # Only allow safe characters
    name = re.sub(r'[^a-zA-Z0-9.\-_\s]', '', name)
    name = name.strip().replace(" ", ".")
    # Collapse multiple dots
    while '..' in name:
        name = name.replace("..", ".")
    return name or "unnamed"


def generate_release_name(metadata: dict, media_type: str, release_group: str = "Torrup") -> str:
    """Generate a standardized release name based on metadata."""
    if media_type == "music":
        artist = sanitize_release_name(metadata.get("artist", "Unknown"))
        album = sanitize_release_name(metadata.get("album", "Unknown"))
        year = metadata.get("year", "")
        source = metadata.get("source", "WEB")
        fmt = metadata.get("format", "MP3")
        bitrate = metadata.get("bitrate", "320")
        
        # Standard: Artist-Album-Year-Source-Format-Bitrate-Group
        # E.g. Post.Malone-Beerbongs.And.Bentleys-2018-WEB-FLAC-24bit-Torrup
        parts = [artist, album]
        if year:
            parts.append(str(year))
        
        parts.append(source)
        
        if fmt == "FLAC":
            parts.append("FLAC")
            parts.append(bitrate) # 16bit or 24bit
        else:
            parts.append(fmt) # MP3
            parts.append(bitrate) # 320 or V0
            
        parts.append(sanitize_release_name(release_group))
        
        return "-".join(parts)
        
    # Default/Fallback for other types
    base_title = metadata.get("title", "Unknown")
    year = metadata.get("year", "")
    if year:
        return sanitize_release_name(f"{base_title}.{year}-{release_group}")
    return sanitize_release_name(f"{base_title}-{release_group}")


def validate_path_for_subprocess(path: Path) -> bool:
    """Validate path is safe for subprocess use."""
    path_str = str(path)
    # Check for null bytes or other dangerous chars
    if '\x00' in path_str:
        return False
    # Ensure path exists and is under expected directories
    try:
        path.resolve()
        return True
    except (OSError, ValueError):
        return False


def suggest_release_name(media_type: str, path: Path) -> str:
    """Suggest a release name based on file/folder name."""
    base = path.stem if path.is_file() else path.name
    return sanitize_release_name(base)


def is_excluded(path: Path, excludes: list[str]) -> bool:
    """Check if path should be excluded based on directory names."""
    parts = {p.lower() for p in path.parts}
    for ex in excludes:
        if ex.lower() in parts:
            return True
    return False
