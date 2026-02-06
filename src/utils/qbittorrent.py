"""qBitTorrent client utility for automated seeding."""

from __future__ import annotations

import os
from pathlib import Path

import qbittorrentapi

from src.db import db, get_setting
from src.logger import logger


def get_qbt_client():
    """Get an authenticated qBitTorrent client based on current settings."""
    with db() as conn:
        enabled = get_setting(conn, "qbt_enabled") == "1"
        if not enabled:
            return None

        # Use environment variables as overrides for security
        url = os.environ.get("QBT_URL") or get_setting(conn, "qbt_url")
        user = os.environ.get("QBT_USER") or get_setting(conn, "qbt_user")
        pwd = os.environ.get("QBT_PASS") or get_setting(conn, "qbt_pass")

    if not url:
        return None

    try:
        qbt_client = qbittorrentapi.Client(
            host=url,
            username=user,
            password=pwd,
            REQUESTS_ARGS={"timeout": (3.1, 10)},
        )
        qbt_client.auth_log_in()
        return qbt_client
    except Exception as e:
        logger.error(f"Failed to connect to qBitTorrent: {e}")
        return None


def add_to_qbt(
    torrent_path: str | Path, save_path: str | Path, category: str | None = None
) -> bool:
    """Add a torrent to qBitTorrent for seeding.

    Args:
        torrent_path: Path to the .torrent file
        save_path: Path to the actual data (must match what qBT expects)
        category: Optional qBT category

    Returns:
        True if added successfully, False otherwise.
    """
    client = get_qbt_client()
    if not client:
        return False

    with db() as conn:
        tag = get_setting(conn, "qbt_tag") or "Torrup"

    try:
        torrent_path = Path(torrent_path)
        if not torrent_path.exists():
            logger.error(f"Torrent file not found for qBT: {torrent_path}")
            return False

        # qBitTorrent expects the parent directory of the content for 'save_path'
        # if the torrent is a multi-file torrent (directory).
        # However, for 'torrup', we are usually creating torrents where the
        # root is the file or directory we selected.

        res = client.torrents_add(
            torrent_files=open(torrent_path, "rb"),
            save_path=str(Path(save_path).parent),
            category=category,
            tags=tag,
            is_paused=False,
            use_auto_torrent_management=False,
        )

        if res == "Ok.":
            logger.info(f"Successfully added to qBitTorrent: {torrent_path.name}")
            return True
        else:
            logger.warning(f"qBitTorrent add returned: {res}")
            return False

    except Exception as e:
        logger.error(f"Error adding to qBitTorrent: {e}")
        return False