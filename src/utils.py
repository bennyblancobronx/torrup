"""Utility functions for file operations and torrent creation."""

from __future__ import annotations

import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from src.config import ANNOUNCE_KEY, TL_TRACKER


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


def get_folder_size(path: Path) -> int:
    """Calculate total size of all files in a directory."""
    total = 0
    for f in path.rglob("*"):
        if f.is_file():
            total += f.stat().st_size
    return total


def sanitize_release_name(name: str) -> str:
    """Clean up release name for torrent naming."""
    name = name.strip().replace(" ", ".")
    name = name.replace("..", ".")
    return name


def suggest_release_name(media_type: str, path: Path) -> str:
    """Suggest a release name based on file/folder name."""
    base = path.stem if path.is_file() else path.name
    return sanitize_release_name(base)


def pick_piece_size(total_bytes: int) -> int:
    """Calculate optimal piece size for torrent based on total size."""
    size_mb = total_bytes / (1024 * 1024)
    if size_mb < 50:
        return 15  # 32KB
    if size_mb < 150:
        return 16  # 64KB
    if size_mb < 350:
        return 17  # 128KB
    if size_mb < 512:
        return 18  # 256KB
    if size_mb < 1024:
        return 19  # 512KB
    if size_mb < 2048:
        return 20  # 1MB
    if size_mb < 4096:
        return 21  # 2MB
    return 22  # 4MB


def generate_nfo(path: Path, release_name: str, out_dir: Path) -> Path:
    """Generate NFO file using mediainfo."""
    nfo_path = out_dir / f"{release_name}.nfo"
    media_extensions = {".flac", ".mp3", ".m4a", ".mkv", ".mp4", ".avi", ".m4v"}
    media_file = None
    for f in path.rglob("*"):
        if f.suffix.lower() in media_extensions:
            media_file = f
            break

    if media_file:
        try:
            result = subprocess.run(
                ["mediainfo", str(media_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            nfo_content = "\n".join(
                line
                for line in result.stdout.split("\n")
                if not line.strip().startswith("Complete name")
            )
        except Exception:
            nfo_content = f"Release: {release_name}\nGenerated: {datetime.now().isoformat()}"
    else:
        nfo_content = f"Release: {release_name}\nGenerated: {datetime.now().isoformat()}"

    nfo_path.write_text(nfo_content)
    return nfo_path


def create_torrent(path: Path, release_name: str, out_dir: Path) -> Path:
    """Create torrent file using mktorrent."""
    output_path = out_dir / f"{release_name}.torrent"
    total_size = get_folder_size(path) if path.is_dir() else path.stat().st_size
    piece_size = pick_piece_size(total_size)
    announce_url = f"{TL_TRACKER}/announce/{ANNOUNCE_KEY}" if ANNOUNCE_KEY else TL_TRACKER

    cmd = [
        "mktorrent",
        "-p",
        "-l",
        str(piece_size),
        "-a",
        announce_url,
        "-s",
        "TorrentLeech.org",
        "-o",
        str(output_path),
        str(path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise Exception(f"mktorrent failed: {result.stderr}")

    return output_path


def write_xml_metadata(
    release_name: str,
    media_type: str,
    path: Path,
    size_bytes: int,
    torrent_path: Path,
    nfo_path: Path,
    tags: str,
    out_dir: Path,
) -> Path:
    """Write XML sidecar file with upload metadata."""
    xml_path = out_dir / f"{release_name}.xml"
    root = ET.Element("tlt")
    ET.SubElement(root, "release_name").text = release_name
    ET.SubElement(root, "media_type").text = media_type
    ET.SubElement(root, "path").text = str(path)
    ET.SubElement(root, "size_bytes").text = str(size_bytes)
    ET.SubElement(root, "size_human").text = human_size(size_bytes)
    ET.SubElement(root, "torrent_path").text = str(torrent_path)
    ET.SubElement(root, "nfo_path").text = str(nfo_path)
    ET.SubElement(root, "tags").text = tags
    ET.SubElement(root, "created_at").text = now_iso()

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    return xml_path


def is_excluded(path: Path, excludes: list[str]) -> bool:
    """Check if path should be excluded based on directory names."""
    parts = {p.lower() for p in path.parts}
    for ex in excludes:
        if ex.lower() in parts:
            return True
    return False
