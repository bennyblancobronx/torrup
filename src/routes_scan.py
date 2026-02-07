"""Scan-related API route handlers."""

from __future__ import annotations

import threading

from flask import jsonify

from src.auto_worker import _scan_root
from src.db import db, get_excludes, get_media_roots
from src.extensions import limiter
from src.logger import logger
from src.routes import bp
from src.utils import now_iso


@bp.route("/api/scan/trigger", methods=["POST"])
@limiter.limit("2 per minute")
def trigger_scan():
    """Trigger a manual scan of enabled media roots."""
    with db() as conn:
        roots = get_media_roots(conn)
        enabled_roots = [r for r in roots if r["enabled"] and r["auto_scan"]]

    if not enabled_roots:
        return jsonify({"error": "No enabled roots with auto-scan on"}), 400

    def run_scan():
        for root in enabled_roots:
            try:
                with db() as conn:
                    excludes = get_excludes(conn)
                    _scan_root(conn, root, excludes)
                    conn.execute(
                        "UPDATE media_roots SET last_scan = ? WHERE media_type = ?",
                        (now_iso(), root["media_type"])
                    )
                    conn.commit()
            except Exception as e:
                logger.error(f"Manual scan error for {root['media_type']}: {e}", exc_info=True)

    threading.Thread(target=run_scan, daemon=True).start()
    return jsonify({"success": True, "message": f"Scan started for {len(enabled_roots)} root(s)"}), 200
