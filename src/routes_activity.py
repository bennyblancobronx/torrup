"""Activity health API route handlers."""

from __future__ import annotations

from flask import jsonify, request

from src.extensions import limiter
from src.db import db
from src.routes import bp
from src.utils.activity import calculate_health, get_monthly_history


@bp.route("/api/activity/health")
@limiter.limit("60 per minute")
def activity_health():
    """Get current month activity health status."""
    with db() as conn:
        return jsonify(calculate_health(conn)), 200


@bp.route("/api/activity/history")
@limiter.limit("30 per minute")
def activity_history():
    """Get monthly upload history for the last N months."""
    months = request.args.get("months", 6, type=int)
    months = max(1, min(24, months))
    with db() as conn:
        return jsonify(get_monthly_history(conn, months)), 200
