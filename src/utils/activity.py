"""Activity health calculation, history, pace estimation, and ntfy notifications."""

from __future__ import annotations

import calendar
import re
import sqlite3
from datetime import datetime, timedelta, timezone

import httpx

from src.db import get_setting, set_setting
from src.logger import logger


def get_month_bounds() -> tuple[str, str]:
    """Return (start_iso, end_iso) for the current UTC month.

    start is first day 00:00:00, end is first day of next month 00:00:00.
    """
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    if now.month == 12:
        end = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc)
    return start.isoformat(), end.isoformat()


def days_remaining_in_month() -> int:
    """Days left in the current UTC month, including today."""
    now = datetime.now(timezone.utc)
    total_days = calendar.monthrange(now.year, now.month)[1]
    return total_days - now.day + 1


def calculate_health(conn: sqlite3.Connection) -> dict:
    """Calculate activity health for the current month.

    Returns dict with: uploads, queued, minimum, projected, needed,
    critical, enforce, days_remaining, pace.
    """
    start, end = get_month_bounds()

    uploads = conn.execute(
        "SELECT COUNT(*) FROM queue WHERE status IN ('success','duplicate') "
        "AND created_at >= ? AND created_at < ?",
        (start, end),
    ).fetchone()[0]

    queued = conn.execute(
        "SELECT COUNT(*) FROM queue WHERE status = 'queued'"
    ).fetchone()[0]

    minimum = int(get_setting(conn, "tl_min_uploads_per_month") or "10")
    enforce = get_setting(conn, "tl_enforce_activity") == "1"

    projected = uploads + queued
    needed = max(0, minimum - projected)
    critical = enforce and projected < minimum

    days_left = days_remaining_in_month()
    pace = estimate_pace(conn)

    return {
        "uploads": uploads,
        "queued": queued,
        "minimum": minimum,
        "projected": projected,
        "needed": needed,
        "critical": critical,
        "enforce": enforce,
        "days_remaining": days_left,
        "pace": pace,
    }


def get_monthly_history(conn: sqlite3.Connection, months: int = 6) -> list[dict]:
    """Get upload counts grouped by YYYY-MM for the last N months.

    Returns list of dicts with 'month' and 'count', ordered chronologically.
    """
    now = datetime.now(timezone.utc)

    # Calculate the start month
    start_month = now.month - months + 1
    start_year = now.year
    while start_month <= 0:
        start_month += 12
        start_year -= 1

    start_dt = datetime(start_year, start_month, 1, tzinfo=timezone.utc)
    start_iso = start_dt.isoformat()

    rows = conn.execute(
        "SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS count "
        "FROM queue WHERE status IN ('success','duplicate') "
        "AND created_at >= ? "
        "GROUP BY month ORDER BY month ASC",
        (start_iso,),
    ).fetchall()

    result_map = {r["month"]: r["count"] for r in rows}

    # Build full list including zero months
    result = []
    y, m = start_year, start_month
    for _ in range(months):
        key = f"{y:04d}-{m:02d}"
        result.append({"month": key, "count": result_map.get(key, 0)})
        m += 1
        if m > 12:
            m = 1
            y += 1

    return result


def estimate_pace(conn: sqlite3.Connection) -> float | None:
    """Estimate uploads per day over the last 7 days.

    Returns None if no uploads in that window.
    """
    now = datetime.now(timezone.utc)
    week_ago_iso = (now - timedelta(days=7)).isoformat()

    count = conn.execute(
        "SELECT COUNT(*) FROM queue WHERE status IN ('success','duplicate') "
        "AND created_at >= ?",
        (week_ago_iso,),
    ).fetchone()[0]

    if count == 0:
        return None
    return round(count / 7.0, 2)


def send_ntfy(url: str, topic: str, title: str, message: str, priority: str = "high") -> bool:
    """Send a push notification via ntfy. Returns True on success."""
    if not url or not topic:
        return False

    if not url.startswith(("http://", "https://")):
        logger.warning("ntfy URL has invalid scheme, skipping")
        return False

    if not re.match(r"^[a-zA-Z0-9_-]+$", topic):
        logger.warning("ntfy topic contains invalid characters, skipping")
        return False

    target = url.rstrip("/") + "/" + topic
    try:
        resp = httpx.post(
            target,
            headers={
                "Title": title,
                "Priority": priority,
            },
            content=message,
            timeout=10,
        )
        return resp.status_code in (200, 201, 202)
    except Exception as e:
        logger.warning(f"ntfy send failed: {e}")
        return False


def check_and_notify_critical(conn: sqlite3.Connection, critical: bool) -> None:
    """Send ntfy notification only on False->True transition of critical state."""
    enabled = get_setting(conn, "ntfy_enabled") == "1"
    if not enabled:
        return

    last_state = get_setting(conn, "tl_last_critical_state") == "1"

    if critical and not last_state:
        url = get_setting(conn, "ntfy_url")
        topic = get_setting(conn, "ntfy_topic")
        send_ntfy(
            url,
            topic,
            "torrup: Activity Warning",
            "Projected uploads are below the monthly minimum. Check your queue.",
        )

    set_setting(conn, "tl_last_critical_state", "1" if critical else "0")
