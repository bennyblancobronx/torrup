"""TorrentLeech API client."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from src.config import ANNOUNCE_KEY, TL_SEARCH_URL, TL_UPLOAD_URL


def check_exists(release_name: str, exact: bool = True) -> bool:
    """Check if release already exists on TorrentLeech."""
    if not ANNOUNCE_KEY:
        return False
    try:
        response = httpx.post(
            TL_SEARCH_URL,
            data={
                "announcekey": ANNOUNCE_KEY,
                "exact": "1" if exact else "0",
                "query": f"'{release_name}'",
            },
            timeout=30,
        )
        # API returns "1" or "0" (often wrapped in double quotes)
        result = response.text.strip().replace('"', '')
        return result == "1"
    except Exception:
        return False


def upload_torrent(
    torrent_path: Path, 
    nfo_path: Path, 
    category: int, 
    tags: str,
    imdb: str | None = None,
    tvmazeid: int | str | None = None,
    tvmazetype: int | str | None = None
) -> dict[str, Any]:
    """Upload torrent to TorrentLeech."""
    if not ANNOUNCE_KEY:
        raise Exception("TL_ANNOUNCE_KEY not configured")

    data = {
        "announcekey": ANNOUNCE_KEY,
        "category": str(category),
        "tags": tags,
    }
    if imdb:
        data["imdb"] = imdb
    if tvmazeid:
        data["tvmazeid"] = str(tvmazeid)
    if tvmazetype:
        data["tvmazetype"] = str(tvmazetype)

    with open(torrent_path, "rb") as torrent_file, open(nfo_path, "rb") as nfo_file:
        response = httpx.post(
            TL_UPLOAD_URL,
            files={
                "torrent": (torrent_path.name, torrent_file, "application/x-bittorrent"),
                "nfo": (nfo_path.name, nfo_file, "text/plain"),
            },
            data=data,
            timeout=60,
        )

    try:
        torrent_id = int(response.text)
        return {"success": True, "torrent_id": torrent_id}
    except ValueError:
        return {"success": False, "error": response.text}
