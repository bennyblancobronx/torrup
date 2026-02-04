"""Queue CLI commands."""

from __future__ import annotations

import time
from pathlib import Path

from src.config import CATEGORY_OPTIONS, MEDIA_TYPES
from src.db import db
from src.utils import now_iso, suggest_release_name
from src.worker import process_queue_item

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 2
EXIT_NOT_FOUND = 3


def cmd_queue_add(cli) -> int:
    """Handle: torrup queue add <media_type> <path>."""
    media_type = cli.args.media_type
    path_str = cli.args.path
    category = getattr(cli.args, "category", None)
    tags = getattr(cli.args, "tags", "") or ""
    release_name = getattr(cli.args, "release_name", None)
    priority = getattr(cli.args, "priority", 0)

    if media_type not in MEDIA_TYPES:
        return cli.error(f"Invalid media type: {media_type}", EXIT_INVALID_ARGS)

    path = Path(path_str)
    if not path.exists():
        return cli.error(f"Path not found: {path}", EXIT_NOT_FOUND)

    if category is None:
        category = CATEGORY_OPTIONS[media_type][0]["id"]

    if not release_name:
        release_name = suggest_release_name(media_type, path)

    with db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO queue (media_type, path, release_name, category, tags, status, message, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'queued', '', ?, ?)
            """,
            (media_type, str(path), release_name, category, tags, now_iso(), now_iso()),
        )
        item_id = cursor.lastrowid
        conn.commit()

    cli.output(
        {"id": item_id, "release_name": release_name},
        f"Added to queue: id={item_id}, release_name={release_name}",
    )
    return EXIT_SUCCESS


def cmd_queue_list(cli) -> int:
    """Handle: torrup queue list."""
    status = getattr(cli.args, "status", None)
    media_type = getattr(cli.args, "media_type", None)
    limit = getattr(cli.args, "limit", 50)
    offset = getattr(cli.args, "offset", 0)

    query = "SELECT * FROM queue WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if media_type:
        query += " AND media_type = ?"
        params.append(media_type)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with db() as conn:
        rows = conn.execute(query, params).fetchall()
        items = [dict(r) for r in rows]

    if cli.json_output:
        cli.output(items)
    else:
        if not items:
            print("Queue is empty")
        for item in items:
            print(f"[{item['id']}] {item['status']:10} {item['release_name']}")
    return EXIT_SUCCESS


def cmd_queue_update(cli) -> int:
    """Handle: torrup queue update <id>."""
    item_id = cli.args.id
    with db() as conn:
        row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return cli.error(f"Queue item not found: {item_id}", EXIT_NOT_FOUND)

        updates = []
        params = []
        if getattr(cli.args, "release_name", None):
            updates.append("release_name = ?")
            params.append(cli.args.release_name)
        if getattr(cli.args, "category", None):
            updates.append("category = ?")
            params.append(cli.args.category)
        if getattr(cli.args, "tags", None) is not None:
            updates.append("tags = ?")
            params.append(cli.args.tags)
        if getattr(cli.args, "status", None):
            updates.append("status = ?")
            params.append(cli.args.status)
        if getattr(cli.args, "priority", None) is not None:
            updates.append("priority = ?")
            params.append(cli.args.priority)

        if updates:
            updates.append("updated_at = ?")
            params.append(now_iso())
            params.append(item_id)
            conn.execute(f"UPDATE queue SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()

    cli.output({"id": item_id, "updated": True}, f"Updated queue item {item_id}")
    return EXIT_SUCCESS


def cmd_queue_delete(cli) -> int:
    """Handle: torrup queue delete <id>."""
    item_id = cli.args.id
    force = getattr(cli.args, "force", False)

    with db() as conn:
        row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return cli.error(f"Queue item not found: {item_id}", EXIT_NOT_FOUND)

        if not force and not cli.quiet:
            confirm = input(f"Delete queue item {item_id}? [y/N] ")
            if confirm.lower() != "y":
                print("Cancelled")
                return EXIT_SUCCESS

        conn.execute("DELETE FROM queue WHERE id = ?", (item_id,))
        conn.commit()

    cli.output({"id": item_id, "deleted": True}, f"Deleted queue item {item_id}")
    return EXIT_SUCCESS


def cmd_queue_run(cli) -> int:
    """Handle: torrup queue run."""
    once = getattr(cli.args, "once", False)
    interval = getattr(cli.args, "interval", 30)

    if not cli.quiet:
        print(f"Starting queue worker (once={once}, interval={interval}s)")

    while True:
        with db() as conn:
            row = conn.execute(
                "SELECT * FROM queue WHERE status = 'queued' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            if row:
                if not cli.quiet:
                    print(f"Processing: {row['release_name']}")
                process_queue_item(conn, row)
                conn.commit()
            elif once:
                if not cli.quiet:
                    print("No items to process")
                break

        if once:
            break
        time.sleep(interval)

    return EXIT_SUCCESS
