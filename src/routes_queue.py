"""Queue-related API route handlers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from flask import jsonify, request

from src.extensions import limiter
from src.config import CATEGORY_OPTIONS, MEDIA_TYPES
from src.db import db, get_media_roots, get_setting
from src.utils import extract_metadata, generate_release_name, now_iso, suggest_release_name
from src.logger import logger
from src.routes import (
    bp,
    sanitize_tags,
    validate_category,
    validate_release_name,
    VALID_FIELDS,
    VALID_STATUSES,
)


@bp.route("/api/queue/add", methods=["POST"])
@limiter.limit("10 per minute")
def add_queue() -> tuple[Any, int]:
    """Add items to upload queue."""
    data = request.json or {}
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "No items provided"}), 400
    ids = _enqueue_items(items)
    return jsonify({"success": True, "ids": ids}), 200


@bp.route("/api/queue")
def list_queue() -> tuple[Any, int]:
    """List all queue items."""
    with db() as conn:
        rows = conn.execute("SELECT * FROM queue ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in rows]), 200


@bp.route("/api/queue/update", methods=["POST"])
@limiter.limit("30 per minute")
def update_queue() -> tuple[Any, int]:
    """Update a queue item."""
    data = request.json or {}
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "Missing id"}), 400

    try:
        item_id = int(item_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid id"}), 400

    updates = []
    params = []

    for field in VALID_FIELDS:
        if field not in data:
            continue

        value = data[field]

        if field == "release_name":
            if value and not validate_release_name(str(value)):
                return jsonify({"error": "Invalid release_name"}), 400
            updates.append("release_name = ?")
            params.append(str(value) if value else "")

        elif field == "category":
            try:
                category = int(value)
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid category"}), 400
            updates.append("category = ?")
            params.append(category)

        elif field == "tags":
            sanitized = sanitize_tags(str(value)) if value else ""
            updates.append("tags = ?")
            params.append(sanitized)

        elif field == "status":
            if value not in VALID_STATUSES:
                return jsonify({"error": "Invalid status"}), 400
            updates.append("status = ?")
            params.append(value)

        elif field == "imdb":
            if value and not re.match(r"^tt\d{7,9}$", str(value)):
                return jsonify({"error": "Invalid IMDB ID format (tt1234567)"}), 400
            updates.append("imdb = ?")
            params.append(str(value) if value else None)

        elif field == "tvmazeid":
            if value and not str(value).isdigit():
                return jsonify({"error": "Invalid TVMaze ID (numbers only)"}), 400
            updates.append("tvmazeid = ?")
            params.append(str(value) if value else None)

        elif field == "tvmazetype":
            if value and str(value) not in ("1", "2"):
                return jsonify({"error": "Invalid TVMaze Type (1 or 2)"}), 400
            updates.append("tvmazetype = ?")
            params.append(str(value) if value else None)

    if not updates:
        return jsonify({"error": "No updates"}), 400

    params.extend([now_iso(), item_id])
    with db() as conn:
        conn.execute(
            f"UPDATE queue SET {', '.join(updates)}, updated_at = ? WHERE id = ?",
            params,
        )
        conn.commit()

    return jsonify({"success": True}), 200


@bp.route("/api/queue/delete", methods=["POST"])
@limiter.limit("20 per minute")
def delete_queue() -> tuple[Any, int]:
    """Delete a queue item."""
    data = request.json or {}
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "Missing id"}), 400

    with db() as conn:
        conn.execute("DELETE FROM queue WHERE id = ?", (item_id,))
        conn.commit()

    return jsonify({"success": True}), 200


@bp.route("/api/queue/retry-all", methods=["POST"])
@limiter.limit("5 per minute")
def retry_all_failed():
    """Reset all failed items to queued."""
    with db() as conn:
        result = conn.execute(
            "UPDATE queue SET status = 'queued', message = '', updated_at = ? WHERE status = 'failed'",
            (now_iso(),),
        )
        count = result.rowcount
        conn.commit()
    return jsonify({"success": True, "count": count}), 200


@bp.route("/api/queue/clear-duplicates", methods=["POST"])
@limiter.limit("5 per minute")
def clear_duplicates():
    """Remove all duplicate items from queue."""
    with db() as conn:
        result = conn.execute("DELETE FROM queue WHERE status = 'duplicate'")
        count = result.rowcount
        conn.commit()
    return jsonify({"success": True, "count": count}), 200


@bp.route("/api/queue/clear-completed", methods=["POST"])
@limiter.limit("5 per minute")
def clear_completed():
    """Remove all completed items from queue."""
    with db() as conn:
        result = conn.execute("DELETE FROM queue WHERE status = 'success'")
        count = result.rowcount
        conn.commit()
    return jsonify({"success": True, "count": count}), 200


@bp.route("/api/queue/clear-all", methods=["POST"])
@limiter.limit("2 per minute")
def clear_all():
    """Clear entire queue. Requires confirm=true."""
    data = request.json or {}
    if not data.get("confirm"):
        return jsonify({"error": "Must pass confirm: true"}), 400
    with db() as conn:
        result = conn.execute("DELETE FROM queue")
        count = result.rowcount
        conn.commit()
    return jsonify({"success": True, "count": count}), 200


def _enqueue_items(items: list[dict[str, Any]]) -> list[int]:
    """Add items to the queue and return their IDs."""
    ids = []
    with db() as conn:
        roots = get_media_roots(conn)
        for item in items:
            media_type = item.get("media_type", "")
            if media_type not in MEDIA_TYPES:
                continue

            path = item.get("path", "")
            if not path:
                continue

            root = next((r for r in roots if r["media_type"] == media_type), None)
            if not root or not root.get("enabled"):
                continue

            path_obj = Path(path)
            root_path = Path(root["path"])
            if '..' in str(path_obj) or not str(path_obj).isprintable():
                continue
            if not path_obj.exists() or path_obj.is_symlink():
                continue
            try:
                resolved_path = path_obj.resolve(strict=False)
                resolved_root = root_path.resolve(strict=False)
                resolved_path.relative_to(resolved_root)
            except (ValueError, RuntimeError):
                continue

            release_name = item.get("release_name") or suggest_release_name(
                media_type, path_obj
            )

            if release_name and not validate_release_name(str(release_name)):
                continue

            try:
                category = int(item["category"])
            except (ValueError, TypeError, KeyError):
                continue

            if not validate_category(category, media_type, CATEGORY_OPTIONS):
                continue

            tags = sanitize_tags(str(item.get("tags", "")))

            imdb = item.get("imdb")
            tvmazeid = item.get("tvmazeid")
            tvmazetype = item.get("tvmazetype")

            if get_setting(conn, "extract_metadata") != "0":
                meta = extract_metadata(path_obj, media_type)
                imdb = imdb or meta.get("imdb")
                tvmazeid = tvmazeid or meta.get("tvmazeid")

                if not item.get("release_name") and meta:
                    release_group = get_setting(conn, "release_group") or "torrup"
                    generated = generate_release_name(meta, media_type, release_group)
                    if generated and generated != "unnamed" and "Unknown" not in generated:
                        release_name = generated
                        if not validate_release_name(str(release_name)):
                            release_name = suggest_release_name(media_type, path_obj)

            now = now_iso()
            cur = conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, imdb, tvmazeid, tvmazetype, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'queued', ?, ?)
                """,
                (media_type, path, release_name, category, tags, imdb, tvmazeid, tvmazetype, now, now),
            )
            ids.append(cur.lastrowid)
        conn.commit()
    return ids
