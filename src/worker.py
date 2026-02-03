"""Background worker for processing upload queue."""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from src.api import check_exists, upload_torrent
from src.db import db, get_output_dir
from src.utils import (
    create_torrent,
    generate_nfo,
    get_folder_size,
    now_iso,
    sanitize_release_name,
    write_xml_metadata,
)


def update_queue_status(
    conn: sqlite3.Connection, item_id: int, status: str, message: str = ""
) -> None:
    """Update queue item status and message."""
    conn.execute(
        "UPDATE queue SET status = ?, message = ?, updated_at = ? WHERE id = ?",
        (status, message, now_iso(), item_id),
    )


def process_queue_item(conn: sqlite3.Connection, item: sqlite3.Row) -> None:
    """Process a single queue item through the upload pipeline."""
    item_id = item["id"]
    media_type = item["media_type"]
    path = Path(item["path"])
    release_name = sanitize_release_name(item["release_name"])
    category = int(item["category"])
    tags = item["tags"]
    out_dir = get_output_dir(conn)

    if not path.exists():
        update_queue_status(conn, item_id, "failed", "Path not found")
        return

    update_queue_status(conn, item_id, "preparing", "Generating NFO + torrent")

    if check_exists(release_name):
        update_queue_status(conn, item_id, "duplicate", "Exact match found on TorrentLeech")
        return

    try:
        nfo_path = generate_nfo(path, release_name, out_dir)
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
        )

        conn.execute(
            """
            UPDATE queue SET torrent_path = ?, nfo_path = ?, xml_path = ?, updated_at = ?
            WHERE id = ?
            """,
            (str(torrent_path), str(nfo_path), str(xml_path), now_iso(), item_id),
        )
        conn.commit()
    except Exception as e:
        update_queue_status(conn, item_id, "failed", f"Prepare failed: {e}")
        return

    update_queue_status(conn, item_id, "uploading", "Uploading to TorrentLeech")

    try:
        result = upload_torrent(Path(torrent_path), Path(nfo_path), category, tags)
        if result.get("success"):
            update_queue_status(conn, item_id, "success", f"Uploaded: {result['torrent_id']}")
        else:
            update_queue_status(conn, item_id, "failed", f"Upload failed: {result.get('error')}")
    except Exception as e:
        update_queue_status(conn, item_id, "failed", f"Upload error: {e}")


def queue_worker() -> None:
    """Main worker loop that processes queued items."""
    while True:
        with db() as conn:
            row = conn.execute(
                "SELECT * FROM queue WHERE status = 'queued' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            if row:
                process_queue_item(conn, row)
        time.sleep(2)
