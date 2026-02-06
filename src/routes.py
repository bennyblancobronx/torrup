"""Flask route handlers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, render_template, request

from src.extensions import limiter

# Security constants
VALID_FIELDS = frozenset(["release_name", "category", "tags", "status", "imdb", "tvmazeid", "tvmazetype"])
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
    extract_metadata,
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


@bp.route('/api/stats')
def stats():
    """Get system statistics for dashboard."""
    try:
        with db() as conn:
            queue_total = conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
            queue_pending = conn.execute("SELECT COUNT(*) FROM queue WHERE status = 'queued'").fetchone()[0]
            
            auto_enabled = get_setting(conn, "enable_auto_upload") == "1"
            auto_interval = get_setting(conn, "auto_scan_interval") or "60"
            
            music_root = conn.execute("SELECT last_scan FROM media_roots WHERE media_type = 'music'").fetchone()
            last_music_scan = music_root["last_scan"] if music_root else None
            if last_music_scan:
                # Format ISO to simpler date
                last_music_scan = last_music_scan.split('.')[0].replace('T', ' ')

            return jsonify({
                "queue_total": queue_total,
                "queue_pending": queue_pending,
                "auto_enabled": auto_enabled,
                "auto_interval": auto_interval,
                "last_music_scan": last_music_scan
            })
    except Exception as e:
        logger.error(f"Stats failed: {e}")
        return jsonify({"error": "Failed to load stats"}), 500


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
        category_options=CATEGORY_OPTIONS,
    )


@bp.route("/history")
def history_page() -> str:
    """Upload history page."""
    return render_template(
        "history.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
        category_options=CATEGORY_OPTIONS,
        media_types=MEDIA_TYPES,
    )


@bp.route("/api/settings", methods=["POST"])
@limiter.limit("5 per minute")
def update_settings() -> tuple[Any, int]:
    """Update application settings."""
    data = request.json or {}
    with db() as conn:
        # Basic settings
        for key in ["browse_base", "output_dir", "exclude_dirs", "release_group", "extract_metadata", "extract_thumbnails", "auto_scan_interval", "enable_auto_upload", "test_mode", "qbt_enabled", "qbt_url", "qbt_user", "qbt_pass", "qbt_auto_add", "qbt_tag", "qbt_auto_source", "qbt_source_categories", "qbt_category_map"]:
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
                UPDATE media_roots SET path = ?, enabled = ?, default_category = ?, auto_scan = ?
                WHERE media_type = ?
                """,
                (
                    row.get("path", ""),
                    1 if row.get("enabled") else 0,
                    int(row.get("default_category", CATEGORY_OPTIONS[media_type][0]["id"])),
                    1 if row.get("auto_scan") else 0,
                    media_type,
                ),
            )

        conn.commit()

    return jsonify({"success": True}), 200


@bp.route("/api/settings/qbt/test", methods=["POST"])
@limiter.limit("5 per minute")
def test_qbt_connection():
    """Test connection to qBitTorrent."""
    from src.utils.qbittorrent import get_qbt_client
    try:
        client = get_qbt_client()
        if client:
            version = client.app.version
            return jsonify({"success": True, "version": version}), 200
        else:
            return jsonify({"success": False, "error": "Failed to connect. Check logs or settings."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


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



# Queue routes are in src/routes_queue.py (split for file size compliance)
import src.routes_queue  # noqa: F401, E402
