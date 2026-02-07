"""Background worker for processing upload queue."""

from __future__ import annotations

import re
import sqlite3
import time
import traceback
from pathlib import Path

from src.api import check_exists, download_torrent, upload_torrent
from src.db import db, get_output_dir, get_setting
from src.logger import logger
from src.utils import (
    create_torrent,
    extract_metadata,
    extract_thumbnail,
    generate_nfo,
    get_folder_size,
    human_size,
    now_iso,
    sanitize_release_name,
    write_xml_metadata,
)
from src.utils.qbittorrent import add_to_qbt


def sanitize_error_message(error: Exception) -> str:
    """Sanitize error message to avoid leaking sensitive info."""
    msg = str(error)
    # Remove file paths
    msg = re.sub(r'/[^\s]+', '[path]', msg)
    # Remove potential secrets patterns
    msg = re.sub(r'(key|token|secret|password)[=:]\s*\S+', r'\1=[redacted]', msg, flags=re.IGNORECASE)
    # Truncate long messages
    if len(msg) > 200:
        msg = msg[:200] + '...'
    return msg


def update_queue_status(
    conn: sqlite3.Connection, item_id: int, status: str, message: str = ""
) -> None:
    """Update queue item status and message."""
    conn.execute(
        "UPDATE queue SET status = ?, message = ?, updated_at = ? WHERE id = ?",
        (status, message, now_iso(), item_id),
    )


def _cleanup_staging(item_id: int, *paths) -> None:
    """Remove staging files from output dir after successful upload."""
    for p in paths:
        if not p:
            continue
        try:
            Path(p).unlink(missing_ok=True)
        except OSError as e:
            logger.warning(f"Item {item_id}: Could not remove {Path(p).name}: {e}")


def process_queue_item(conn: sqlite3.Connection, item: sqlite3.Row) -> None:
    """Process a single queue item through the upload pipeline."""
    item_id = item["id"]
    media_type = item["media_type"]
    path = Path(item["path"])
    release_name = sanitize_release_name(item["release_name"])
    category = int(item["category"])
    tags = item["tags"]
    out_dir = get_output_dir(conn)
    release_group = get_setting(conn, "release_group") or "torrup"

    logger.info(f"Processing queue item {item_id}: {release_name}")

    if not path.exists():
        logger.warning(f"Item {item_id}: Path not found - {path}")
        update_queue_status(conn, item_id, "failed", "Path not found")
        return

    test_mode = get_setting(conn, "test_mode") == "1"

    update_queue_status(conn, item_id, "preparing", "Generating NFO + torrent")

    if not test_mode and check_exists(release_name):
        update_queue_status(conn, item_id, "duplicate", "Exact match found on TorrentLeech")
        return

    try:
        # Extract metadata using exiftool
        metadata = {}
        if get_setting(conn, "extract_metadata") != "0":
            metadata = extract_metadata(path, media_type)

        # Extract thumbnail/artwork using ffmpeg
        thumb_path = None
        if get_setting(conn, "extract_thumbnails") != "0":
            thumb_path = extract_thumbnail(path, out_dir, release_name, media_type)
            if thumb_path and media_type == "music":
                if not metadata:
                    metadata = {}
                try:
                    size = thumb_path.stat().st_size
                    metadata["album_art_file"] = {"name": thumb_path.name, "size": human_size(size)}
                except OSError:
                    metadata["album_art_file"] = {"name": thumb_path.name}

        nfo_path = generate_nfo(
            path, release_name, out_dir, media_type, release_group, metadata
        )
        torrent_path = create_torrent(path, release_name, out_dir)
        size_bytes = get_folder_size(path) if path.is_dir() else path.stat().st_size
        xml_path = write_xml_metadata(
            release_name,
            media_type,
            path,
            size_bytes,
            torrent_path,
            nfo_path,
            tags,
            out_dir,
            metadata,
            thumb_path,
        )

        conn.execute(
            """
            UPDATE queue SET torrent_path = ?, nfo_path = ?, xml_path = ?, thumb_path = ?, updated_at = ?
            WHERE id = ?
            """,
            (str(torrent_path), str(nfo_path), str(xml_path), str(thumb_path) if thumb_path else None, now_iso(), item_id),
        )
        conn.commit()
        logger.info(f"Item {item_id}: Preparation complete - torrent and NFO generated")
    except Exception as e:
        logger.error(f"Item {item_id}: Prepare failed - {e}\n{traceback.format_exc()}")
        update_queue_status(conn, item_id, "failed", f"Prepare failed: {sanitize_error_message(e)}")
        return

    if test_mode:
        logger.info(f"Item {item_id}: Test mode - skipping upload")
        update_queue_status(conn, item_id, "success", "Test mode - upload skipped")
        return

    update_queue_status(conn, item_id, "uploading", "Uploading to TorrentLeech")

    try:
        # Extract metadata for API - only use movie/TV fields for those media types
        if media_type in ("movies", "tv"):
            imdb = metadata.get("imdb")
            tvmazeid = metadata.get("tvmazeid")
            tvmazetype = metadata.get("tvmazetype")

            # Auto-detect tvmazetype if not set: 1 for boxsets (if path is dir), 2 for episodes
            if tvmazeid and not tvmazetype:
                tvmazetype = 1 if path.is_dir() else 2
        else:
            imdb = None
            tvmazeid = None
            tvmazetype = None

        result = upload_torrent(
            Path(torrent_path),
            Path(nfo_path),
            category,
            tags,
            imdb=imdb,
            tvmazeid=tvmazeid,
            tvmazetype=tvmazetype
        )
        if result.get("success"):
            tid = result["torrent_id"]
            logger.info(f"Item {item_id}: Upload successful - torrent_id={tid}")
            update_queue_status(conn, item_id, "success", f"Uploaded: {tid}")

            # Auto-seed via qBitTorrent: download TL's official .torrent
            # (hash may differ from local mktorrent output) and feed to qBT.
            if get_setting(conn, "qbt_enabled") == "1":
                tl_torrent = out_dir / f"{release_name}.tl.torrent"
                if download_torrent(tid, tl_torrent):
                    add_to_qbt(tl_torrent, path)
                else:
                    logger.warning(f"Item {item_id}: TL torrent download failed, seeding with local copy")
                    add_to_qbt(torrent_path, path)

            # Clean up staging files -- output dir is a cache, not permanent storage
            _cleanup_staging(item_id, torrent_path, nfo_path, xml_path, thumb_path)
        else:
            logger.warning(f"Item {item_id}: Upload failed - {result.get('error')}")
            update_queue_status(conn, item_id, "failed", f"Upload failed: {result.get('error')}")
    except Exception as e:
        logger.error(f"Item {item_id}: Upload error - {e}\n{traceback.format_exc()}")
        update_queue_status(conn, item_id, "failed", f"Upload error: {sanitize_error_message(e)}")


def queue_worker(shutdown_event: "threading.Event | None" = None) -> None:
    """Main worker loop that processes queued items.

    Args:
        shutdown_event: Optional event that signals the worker to stop.
    """
    import threading as _threading

    if shutdown_event is None:
        shutdown_event = _threading.Event()

    logger.info("Queue worker started")
    backoff = 2
    max_backoff = 60
    while not shutdown_event.is_set():
        try:
            processed = False
            with db() as conn:
                row = conn.execute(
                    "SELECT * FROM queue WHERE status = 'queued' AND approval_status = 'approved' ORDER BY id ASC LIMIT 1"
                ).fetchone()
                if row:
                    process_queue_item(conn, row)
                    processed = True
            if processed:
                try:
                    from src.utils.activity import calculate_health, check_and_notify_critical
                    with db() as notify_conn:
                        health = calculate_health(notify_conn)
                        check_and_notify_critical(notify_conn, health["critical"])
                except Exception as e:
                    logger.warning(f"Activity notification check failed: {e}")
            backoff = 2  # Reset backoff on success
            shutdown_event.wait(2)
        except Exception as e:
            logger.error(f"Worker loop error: {e}", exc_info=True)
            shutdown_event.wait(backoff)
            backoff = min(backoff * 2, max_backoff)  # Exponential backoff
    logger.info("Queue worker stopped")
