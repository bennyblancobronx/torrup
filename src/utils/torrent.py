"""Torrent creation utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path

from src.config import ANNOUNCE_KEY, TL_TRACKER
from src.utils.core import get_folder_size, validate_path_for_subprocess


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


def create_torrent(path: Path, release_name: str, out_dir: Path) -> Path:
    """Create torrent file using mktorrent."""
    output_path = out_dir / f"{release_name}.torrent"
    total_size = get_folder_size(path) if path.is_dir() else path.stat().st_size
    piece_size = pick_piece_size(total_size)
    # TL docs specify personalized announce URLs in the form /a/<passkey>/announce
    announce_url = (
        f"{TL_TRACKER}/a/{ANNOUNCE_KEY}/announce" if ANNOUNCE_KEY else TL_TRACKER
    )

    # Validate paths before subprocess call
    if not validate_path_for_subprocess(path):
        raise ValueError(f"Invalid path for torrent creation: {path}")
    if not validate_path_for_subprocess(output_path):
        raise ValueError(f"Invalid output path for torrent creation: {output_path}")

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

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise Exception(f"mktorrent failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        raise Exception("mktorrent timed out after 120 seconds")
    except subprocess.SubprocessError as e:
        raise Exception(f"mktorrent subprocess error: {e}")

    return output_path
