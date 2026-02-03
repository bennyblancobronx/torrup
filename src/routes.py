"""Flask route handlers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, render_template, request

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

bp = Blueprint("main", __name__)


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


@bp.route("/api/settings", methods=["POST"])
def update_settings() -> tuple[Any, int]:
    """Update application settings."""
    data = request.json or {}
    with db() as conn:
        # Basic settings
        for key in ["browse_base", "output_dir", "exclude_dirs"]:
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

    # Security: ensure path is under root
    try:
        path.resolve().relative_to(root_path.resolve())
    except Exception:
        return jsonify({"error": "Access denied"}), 403

    if not path.exists():
        return jsonify({"error": "Path not found"}), 404

    items = []
    if path.is_dir():
        for item in sorted(path.iterdir()):
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
def update_queue() -> tuple[Any, int]:
    """Update a queue item."""
    data = request.json or {}
    item_id = data.get("id")
    if not item_id:
        return jsonify({"error": "Missing id"}), 400

    updates = []
    params = []
    for field in ["release_name", "category", "tags", "status"]:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])

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
            media_type = item["media_type"]
            path = item["path"]
            release_name = item.get("release_name") or suggest_release_name(
                media_type, Path(path)
            )
            category = int(item["category"])
            tags = item.get("tags", "")
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
