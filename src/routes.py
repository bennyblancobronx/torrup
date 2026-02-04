"""Flask route handlers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, render_template, request

from src.extensions import limiter

# Security constants
VALID_FIELDS = frozenset(["release_name", "category", "tags", "status"])
VALID_STATUSES = frozenset(["queued", "preparing", "uploading", "success", "failed", "duplicate"])


def sanitize_tags(tags: str) -> str:
    """Allow only alphanumeric, spaces, commas, hyphens."""
    return re.sub(r'[^a-zA-Z0-9,\s\-]', '', tags)


def validate_release_name(name: str) -> bool:
    """Ensure release name has no path traversal."""
    if not name or '..' in name or '/' in name or '\\' in name:
        return False
    return True


def validate_category(category: Any, media_type: str, category_options: dict) -> bool:
    """Validate category is a valid integer for the media type."""
    try:
        cat_id = int(category)
        valid_ids = [opt["id"] for opt in category_options.get(media_type, [])]
        return cat_id in valid_ids
    except (ValueError, TypeError):
        return False

from src.config import (
    APP_NAME,
    APP_VERSION,
    CATEGORY_OPTIONS,
    DEFAULT_TEMPLATES,
    MEDIA_TYPES,
)
from src.db import db, get_excludes, get_media_roots, get_setting, set_setting
from src.utils import (
    get_folder_size,
    human_size,
    is_excluded,
    now_iso,
    suggest_release_name,
)
from src.logger import logger

bp = Blueprint("main", __name__)


@bp.route('/health')
def health():
    """Health check endpoint for monitoring."""
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "healthy", "version": APP_VERSION}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy"}), 503


@bp.route("/")
def index() -> str:
    """Main upload UI page."""
    return render_template(
        "index.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
        media_types=MEDIA_TYPES,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/settings")
def settings() -> str:
    """Settings UI page."""
    with db() as conn:
        settings_rows = conn.execute("SELECT key, value FROM settings").fetchall()
        media_roots = get_media_roots(conn)
        templates = {k: get_setting(conn, f"template_{k}") for k in DEFAULT_TEMPLATES}
    return render_template(
        "settings.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
        settings={r["key"]: r["value"] for r in settings_rows},
        media_roots=media_roots,
        templates=templates,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/browse")
def browse_page() -> str:
    """Browse media library page."""
    with db() as conn:
        media_roots = get_media_roots(conn)
    return render_template(
        "browse.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
        media_types=MEDIA_TYPES,
        media_roots=media_roots,
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/queue")
def queue_page() -> str:
    """Upload queue page."""
    return render_template(
        "queue.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
    )


@bp.route("/history")
def history_page() -> str:
    """Upload history page."""
    return render_template(
        "history.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
    )


@bp.route("/api/settings", methods=["POST"])
@limiter.limit("5 per minute")
def update_settings() -> tuple[Any, int]:
    """Update application settings."""
    data = request.json or {}
    with db() as conn:
        # Basic settings
        for key in ["browse_base", "output_dir", "exclude_dirs", "release_group", "extract_metadata", "extract_thumbnails"]:
            if key in data:
                set_setting(conn, key, str(data[key]))

        # Templates
        templates = data.get("templates", {})
        for k, v in templates.items():
            if k in DEFAULT_TEMPLATES:
                set_setting(conn, f"template_{k}", v)

        # Media roots
        for row in data.get("media_roots", []):
            media_type = row.get("media_type")
            if media_type not in MEDIA_TYPES:
                continue
            conn.execute(
                """
                UPDATE media_roots SET path = ?, enabled = ?, default_category = ?
                WHERE media_type = ?
                """,
                (
                    row.get("path", ""),
                    1 if row.get("enabled") else 0,
                    int(row.get("default_category", CATEGORY_OPTIONS[media_type][0]["id"])),
                    media_type,
                ),
            )

        conn.commit()

    return jsonify({"success": True}), 200


@bp.route("/api/browse")
@limiter.limit("60 per minute")
def browse() -> tuple[Any, int]:
    """Browse media library folders."""
    media_type = request.args.get("media_type", "music")
    path_str = request.args.get("path", "")

    with db() as conn:
        roots = get_media_roots(conn)
        excludes = get_excludes(conn)

    root = next((r for r in roots if r["media_type"] == media_type), None)
    if not root or not root.get("enabled"):
        return jsonify({"error": "Media type disabled"}), 400

    root_path = Path(root["path"])
    path = Path(path_str) if path_str else root_path

    # Security: ensure path is under root and no traversal
    if '..' in str(path) or not str(path).isprintable():
        return jsonify({"error": "Invalid path"}), 400

    try:
        resolved_path = path.resolve(strict=False)
        resolved_root = root_path.resolve(strict=False)
        resolved_path.relative_to(resolved_root)
    except (ValueError, RuntimeError):
        return jsonify({"error": "Access denied"}), 403

    # Reject symlinks to prevent directory traversal
    if path.is_symlink():
        return jsonify({"error": "Symlinks not allowed"}), 403

    if not path.exists():
        return jsonify({"error": "Path not found"}), 404

    items = []
    if path.is_dir():
        for item in sorted(path.iterdir()):
            if item.is_symlink():
                continue
            if is_excluded(item, excludes):
                continue
            try:
                is_dir = item.is_dir()
                size = get_folder_size(item) if is_dir else item.stat().st_size
                items.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "is_dir": is_dir,
                        "size": human_size(size),
                        "size_bytes": size,
                    }
                )
            except PermissionError:
                continue
            except ValueError:
                # Directory has too many files, show with unknown size
                items.append(
                    {
                        "name": item.name,
                        "path": str(item),
                        "is_dir": is_dir,
                        "size": "Too many files",
                        "size_bytes": -1,
                    }
                )

    return (
        jsonify(
            {
                "path": str(path),
                "parent": str(path.parent) if path != root_path else None,
                "items": items,
                "root": str(root_path),
                "default_category": root.get("default_category"),
            }
        ),
        200,
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

    # Validate item_id is integer
    try:
        item_id = int(item_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid id"}), 400

    updates = []
    params = []

    # Validate and process each field
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


def _enqueue_items(items: list[dict[str, Any]]) -> list[int]:
    """Add items to the queue and return their IDs."""
    ids = []
    with db() as conn:
        for item in items:
            media_type = item.get("media_type", "")
            if media_type not in MEDIA_TYPES:
                continue

            path = item.get("path", "")
            if not path:
                continue

            release_name = item.get("release_name") or suggest_release_name(
                media_type, Path(path)
            )

            # Validate release_name
            if release_name and not validate_release_name(str(release_name)):
                continue

            # Validate category
            try:
                category = int(item["category"])
            except (ValueError, TypeError, KeyError):
                continue

            if not validate_category(category, media_type, CATEGORY_OPTIONS):
                continue

            # Sanitize tags
            tags = sanitize_tags(str(item.get("tags", "")))

            now = now_iso()
            cur = conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'queued', ?, ?)
                """,
                (media_type, path, release_name, category, tags, now, now),
            )
            ids.append(cur.lastrowid)
        conn.commit()
    return ids
