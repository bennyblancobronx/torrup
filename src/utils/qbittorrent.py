"""qBitTorrent client utility for automated seeding."""

from __future__ import annotations

import os
import json
from pathlib import Path
from urllib.parse import urlparse

import qbittorrentapi

from src.db import db, get_setting
from src.logger import logger


def _normalize_qbt_url(url: str) -> str | None:
    url = (url or "").strip()
    if not url:
        return None
    if "://" not in url:
        url = f"http://{url}"
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return None
    return url


def parse_qbt_category_map(value: str | None) -> dict[str, str]:
    """Parse qBT category mapping from JSON or CSV.

    Supported formats:
    - JSON: {"movies": "Movies-HD", "music": "Music"}
    - CSV: movies=Movies-HD,music=Music
    """
    raw = (value or "").strip()
    if not raw:
        return {}

    if raw.startswith("{"):
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return {str(k).strip(): str(v).strip() for k, v in data.items() if str(k).strip()}
        except json.JSONDecodeError:
            logger.warning("Invalid qBT category map JSON; falling back to CSV parsing.")

    mapping: dict[str, str] = {}
    for pair in raw.split(","):
        if "=" not in pair:
            continue
        key, val = pair.split("=", 1)
        key = key.strip()
        val = val.strip()
        if key:
            mapping[key] = val
    return mapping


def map_media_type_to_qbt_category(media_type: str, mapping_value: str | None) -> str:
    mapping = parse_qbt_category_map(mapping_value)
    return mapping.get(media_type, media_type)


def map_qbt_category_to_media_type(qbt_category: str, mapping_value: str | None) -> str | None:
    mapping = parse_qbt_category_map(mapping_value)
    if not mapping:
        return None
    target = (qbt_category or "").strip().lower()
    if not target:
        return None
    for media_type, cat in mapping.items():
        if cat.strip().lower() == target:
            return media_type
    return None


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

    url = _normalize_qbt_url(url)
    if not url:
        logger.error("qBT URL is missing or invalid. Set qbt_url or QBT_URL.")
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
        if isinstance(e, getattr(qbittorrentapi, "LoginFailed", Exception)):
            logger.error("qBT login failed. Check qbt_user/qbt_pass or QBT_USER/QBT_PASS.")
        else:
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
        tag = get_setting(conn, "qbt_tag") or "torrup"

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
