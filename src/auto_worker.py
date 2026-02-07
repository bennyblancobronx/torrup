"""Background worker for automated media scanning and queuing."""

from __future__ import annotations

import time
from pathlib import Path

from src.api import check_exists
from src.cli.queue import calculate_certainty
from src.db import db, get_media_roots, get_setting, get_excludes
from src.logger import logger
from src.utils import (
    extract_metadata,
    generate_release_name,
    is_excluded,
    now_iso,
    sanitize_release_name,
    suggest_release_name,
)



def auto_scan_worker(shutdown_event: "threading.Event | None" = None) -> None:
    """Periodically scans enabled media roots for new content and queues them if missing on TL.

    Args:
        shutdown_event: Optional event that signals the worker to stop.
    """
    import threading as _threading

    if shutdown_event is None:
        shutdown_event = _threading.Event()

    logger.info("Auto-scan worker started")

    while not shutdown_event.is_set():
        try:
            with db() as conn:
                enabled = get_setting(conn, "enable_auto_upload") == "1"
                interval_mins = int(get_setting(conn, "auto_scan_interval") or 60)
                excludes = get_excludes(conn)

                if not enabled:
                    shutdown_event.wait(60)
                    continue

                roots = get_media_roots(conn)
                for root in roots:
                    if shutdown_event.is_set():
                        break
                    if not root["auto_scan"]:
                        continue

                    # Check if it's time to scan this root
                    last_scan = root["last_scan"]
                    if last_scan:
                        # Simple check: has interval passed?
                        pass  # For now we just scan every loop if auto_scan is on

                    logger.info(f"Auto-scanning {root['media_type']} root: {root['path']}")
                    _scan_root(conn, root, excludes)

                    # Update last scan time
                    conn.execute(
                        "UPDATE media_roots SET last_scan = ? WHERE media_type = ?",
                        (now_iso(), root["media_type"])
                    )

            # Wait for next interval
            shutdown_event.wait(interval_mins * 60)

        except Exception as e:
            logger.error(f"Auto-scan worker error: {e}", exc_info=True)
            shutdown_event.wait(300)  # Wait 5 mins on error

    logger.info("Auto-scan worker stopped")


def _scan_root(conn, root, excludes, source="Auto-scan"):
    """Scan a specific root directory."""
    base_path = Path(root["path"])
    if not base_path.exists():
        return

    media_type = root["media_type"]
    category = root["default_category"]
    release_group = get_setting(conn, "release_group") or "torrup"

    # For music, scan two levels deep (Artist/Album).
    # For other types, scan immediate children only.
    if media_type == "music":
        entries = []
        for artist_dir in base_path.iterdir():
            if not artist_dir.is_dir() or is_excluded(artist_dir, excludes):
                continue
            for album_dir in artist_dir.iterdir():
                if album_dir.is_dir() and not is_excluded(album_dir, excludes):
                    entries.append(album_dir)
    else:
        entries = [e for e in base_path.iterdir() if not is_excluded(e, excludes)]

    for entry in entries:
        try:
            # Check if already in queue or history
            exists_in_db = conn.execute(
                "SELECT 1 FROM queue WHERE path = ?", (str(entry),)
            ).fetchone()

            if exists_in_db:
                continue

            metadata = extract_metadata(entry, media_type)
            release_name = generate_release_name(metadata, media_type, release_group)
            if not release_name or release_name == "unnamed" or "Unknown" in release_name:
                release_name = suggest_release_name(media_type, entry)

            if not release_name:
                continue

            # Check TL (exact=False for fuzzy matching, rate-limited)
            if check_exists(release_name, exact=False):
                logger.info(f"{source}: {release_name} already on TL, skipping.")
                _add_to_queue_silent(
                    conn, media_type, entry, release_name,
                    category, "duplicate", "Found during auto-scan", metadata,
                )
                conn.commit()
                time.sleep(1.5)
                continue

            time.sleep(1.5)

            # Not on TL, add to queue
            logger.info(f"{source}: Found new content {release_name}, adding to queue.")
            _add_to_queue(conn, media_type, entry, release_name, category, metadata)
            conn.commit()
        except Exception as e:
            logger.error(f"{source}: Error processing {entry}: {e}")
            continue


def _add_to_queue(conn, media_type, path, release_name, category, metadata):
    """Add item to queue for processing with certainty scoring."""
    certainty = calculate_certainty(metadata, media_type)
    approval = "approved" if certainty >= 80 else "pending_approval"

    conn.execute(
        """
        INSERT INTO queue (
            media_type, path, release_name, category,
            imdb, tvmazeid, tvmazetype,
            created_at, updated_at, status,
            certainty_score, approval_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'queued', ?, ?)
        """,
        (
            media_type,
            str(path),
            release_name,
            category,
            metadata.get("imdb"),
            metadata.get("tvmazeid"),
            metadata.get("tvmazetype"),
            now_iso(),
            now_iso(),
            certainty,
            approval,
        )
    )


def _add_to_queue_silent(conn, media_type, path, release_name, category, status, message, metadata):
    """Add item to queue with a specific status (e.g. duplicate) to avoid re-scanning."""
    conn.execute(
        """
        INSERT INTO queue (media_type, path, release_name, category, imdb, tvmazeid, tvmazetype, created_at, updated_at, status, message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            media_type,
            str(path),
            release_name,
            category,
            metadata.get("imdb"),
            metadata.get("tvmazeid"),
            metadata.get("tvmazetype"),
            now_iso(),
            now_iso(),
            status,
            message
        )
    )
