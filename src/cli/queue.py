"""Queue CLI commands."""

from __future__ import annotations

import time
from pathlib import Path

from src.api import check_exists
from src.config import CATEGORY_OPTIONS, MEDIA_TYPES
from src.db import db, get_setting
from src.utils import generate_release_name, now_iso, suggest_release_name
from src.utils.metadata import extract_metadata
from src.worker import process_queue_item

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 2
EXIT_NOT_FOUND = 3


def calculate_certainty(metadata: dict, media_type: str) -> int:
    """Calculate certainty score (0-100) based on metadata quality."""
    score = 0
    if media_type == "music":
        # Core fields (weighted by importance for correct release naming)
        if metadata.get("artist"): score += 30
        if metadata.get("album"): score += 30
        if metadata.get("year"): score += 15
        if metadata.get("format"): score += 15  # Any detected format
        if metadata.get("bitrate"): score += 10
    else:
        # Generic/Movie/TV
        if metadata.get("title"): score += 40
        if metadata.get("year"): score += 30
        if metadata.get("imdb") or metadata.get("tvmazeid"): score += 30

    return max(0, min(100, score))


def cmd_queue_add(cli) -> int:
    """Handle: torrup queue add <media_type> <path>."""
    media_type = cli.args.media_type
    path_str = cli.args.path
    category = getattr(cli.args, "category", None)
    tags = getattr(cli.args, "tags", "") or ""
    release_name = getattr(cli.args, "release_name", None)

    if media_type not in MEDIA_TYPES:
        return cli.error(f"Invalid media type: {media_type}", EXIT_INVALID_ARGS)

    path = Path(path_str)
    if not path.exists():
        return cli.error(f"Path not found: {path}", EXIT_NOT_FOUND)

    if category is None:
        category = CATEGORY_OPTIONS[media_type][0]["id"]

    # Enhanced logic
    certainty = 100
    approval = "approved"
    
    # 1. Extract Metadata
    try:
        meta = extract_metadata(path, media_type)
    except Exception:
        meta = {}

    # 2. Generate Name (if not overridden)
    if not release_name:
        with db() as conn:
            group = get_setting(conn, "release_group") or "Torrup"
        release_name = generate_release_name(meta, media_type, group)
        # Fallback if metadata empty
        if release_name == "unnamed" or release_name.startswith("Unknown"):
            release_name = suggest_release_name(media_type, path)

    # 3. Calculate Certainty
    certainty = calculate_certainty(meta, media_type)
    if certainty < 80:
        approval = "pending_approval"

    with db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO queue (
                media_type, path, release_name, category, tags, status, 
                message, created_at, updated_at, certainty_score, approval_status
            )
            VALUES (?, ?, ?, ?, ?, 'queued', '', ?, ?, ?, ?)
            """,
            (media_type, str(path), release_name, category, tags, now_iso(), now_iso(), certainty, approval),
        )
        item_id = cursor.lastrowid
        conn.commit()

    cli.output(
        {"id": item_id, "release_name": release_name, "certainty": certainty, "approval": approval},
        f"Added to queue: id={item_id}, release={release_name}, certainty={certainty}%, status={approval}",
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
            q_str = f"[{item['certainty_score']}%]"
            print(f"[{item['id']}] {item['status']:10} {q_str:6} {item['release_name']}")
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
        if getattr(cli.args, "approval", None):
            updates.append("approval_status = ?")
            params.append(cli.args.approval)

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
            # Only process approved items
            row = conn.execute(
                "SELECT * FROM queue WHERE status = 'queued' AND approval_status = 'approved' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            if row:
                if not cli.quiet:
                    print(f"Processing: {row['release_name']}")
                process_queue_item(conn, row)
                conn.commit()
            elif once:
                if not cli.quiet:
                    print("No approved items to process")
                break

        if once:
            break
        time.sleep(interval)

    return EXIT_SUCCESS
