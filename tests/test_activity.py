"""Tests for TorrentLeech activity enforcement."""

from __future__ import annotations

import importlib
import json
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

import pytest


def insert_queue_item(conn, status, created_at, media_type="music"):
    """Insert a test queue item with given status and created_at."""
    conn.execute(
        "INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at) "
        "VALUES (?, '/test/path', 'Test-Release', 31, '', ?, ?, ?)",
        (media_type, status, created_at, created_at),
    )


def current_month_iso(day=15):
    """Return an ISO timestamp within the current month."""
    now = datetime.now(timezone.utc)
    dt = datetime(now.year, now.month, min(day, 28), 12, 0, 0, tzinfo=timezone.utc)
    return dt.isoformat()


def last_month_iso(day=15):
    """Return an ISO timestamp from last month."""
    now = datetime.now(timezone.utc)
    if now.month == 1:
        dt = datetime(now.year - 1, 12, day, 12, 0, 0, tzinfo=timezone.utc)
    else:
        dt = datetime(now.year, now.month - 1, min(day, 28), 12, 0, 0, tzinfo=timezone.utc)
    return dt.isoformat()


# --------------------------------------------------------------------------
# TestMonthBounds
# --------------------------------------------------------------------------

class TestMonthBounds:
    def test_returns_tuple(self):
        from src.utils.activity import get_month_bounds
        start, end = get_month_bounds()
        assert isinstance(start, str)
        assert isinstance(end, str)

    def test_start_is_first_of_month(self):
        from src.utils.activity import get_month_bounds
        start, _ = get_month_bounds()
        dt = datetime.fromisoformat(start)
        assert dt.day == 1
        assert dt.hour == 0
        assert dt.minute == 0

    def test_end_is_first_of_next_month(self):
        from src.utils.activity import get_month_bounds
        start, end = get_month_bounds()
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        if start_dt.month == 12:
            assert end_dt.month == 1
            assert end_dt.year == start_dt.year + 1
        else:
            assert end_dt.month == start_dt.month + 1

    def test_format_is_iso(self):
        from src.utils.activity import get_month_bounds
        start, end = get_month_bounds()
        # Should parse without error
        datetime.fromisoformat(start)
        datetime.fromisoformat(end)

    def test_december_rolls_to_january_next_year(self):
        """When current month is December, end boundary is Jan 1 of next year."""
        from src.utils.activity import get_month_bounds

        fake_now = datetime(2025, 12, 15, 10, 30, 0, tzinfo=timezone.utc)

        # Build a mock that intercepts datetime.now() but delegates
        # constructor calls to the real datetime class.
        real_datetime = datetime

        class FakeDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return fake_now

        with patch("src.utils.activity.datetime", FakeDatetime):
            start, end = get_month_bounds()

        start_dt = real_datetime.fromisoformat(start)
        end_dt = real_datetime.fromisoformat(end)

        assert start_dt == real_datetime(2025, 12, 1, tzinfo=timezone.utc)
        assert end_dt == real_datetime(2026, 1, 1, tzinfo=timezone.utc)
        assert end_dt.month == 1
        assert end_dt.year == start_dt.year + 1


class TestDaysRemaining:
    def test_returns_positive_int(self):
        from src.utils.activity import days_remaining_in_month
        result = days_remaining_in_month()
        assert isinstance(result, int)
        assert result >= 1

    def test_max_is_31(self):
        from src.utils.activity import days_remaining_in_month
        result = days_remaining_in_month()
        assert result <= 31


# --------------------------------------------------------------------------
# TestHealthCalculation
# --------------------------------------------------------------------------

class TestHealthCalculation:
    def test_zero_state(self, client):
        """No uploads, no queued items -- should be critical."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["uploads"] == 0
        assert health["queued"] == 0
        assert health["minimum"] == 10
        assert health["projected"] == 0
        assert health["needed"] == 10
        assert health["critical"] is True
        assert health["enforce"] is True
        assert health["days_remaining"] >= 1

    def test_with_uploads(self, client):
        """Some successful uploads this month."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        ts = current_month_iso()
        with db_module.db() as conn:
            for _ in range(5):
                insert_queue_item(conn, "success", ts)
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["uploads"] == 5
        assert health["projected"] == 5
        assert health["needed"] == 5
        assert health["critical"] is True

    def test_with_queued(self, client):
        """Queued items count toward projected."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        ts = current_month_iso()
        with db_module.db() as conn:
            for _ in range(5):
                insert_queue_item(conn, "success", ts)
            for _ in range(5):
                insert_queue_item(conn, "queued", ts)
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["uploads"] == 5
        assert health["queued"] == 5
        assert health["projected"] == 10
        assert health["needed"] == 0
        assert health["critical"] is False

    def test_mixed_statuses(self, client):
        """Only success and duplicate count as uploads."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        ts = current_month_iso()
        with db_module.db() as conn:
            for _ in range(3):
                insert_queue_item(conn, "success", ts)
            for _ in range(2):
                insert_queue_item(conn, "duplicate", ts)
            for _ in range(4):
                insert_queue_item(conn, "failed", ts)
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["uploads"] == 5

    def test_previous_month_excluded(self, client):
        """Items from last month should not count."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        last = last_month_iso()
        with db_module.db() as conn:
            for _ in range(10):
                insert_queue_item(conn, "success", last)
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["uploads"] == 0

    def test_enforce_toggle(self, client):
        """When enforce is off, critical should be False."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        with db_module.db() as conn:
            db_module.set_setting(conn, "tl_enforce_activity", "0")
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["enforce"] is False
        assert health["critical"] is False

    def test_needed_calc(self, client):
        """Needed is max(0, minimum - projected)."""
        import src.db as db_module
        from src.utils.activity import calculate_health

        ts = current_month_iso()
        with db_module.db() as conn:
            for _ in range(15):
                insert_queue_item(conn, "success", ts)
            conn.commit()

        with db_module.db() as conn:
            health = calculate_health(conn)

        assert health["needed"] == 0
        assert health["critical"] is False


# --------------------------------------------------------------------------
# TestMonthlyHistory
# --------------------------------------------------------------------------

class TestMonthlyHistory:
    def test_empty(self, client):
        """No uploads returns list with zero counts."""
        import src.db as db_module
        from src.utils.activity import get_monthly_history

        with db_module.db() as conn:
            history = get_monthly_history(conn, 3)

        assert isinstance(history, list)
        assert len(history) == 3
        for entry in history:
            assert "month" in entry
            assert "count" in entry

    def test_grouped_by_month(self, client):
        """Uploads are grouped by month."""
        import src.db as db_module
        from src.utils.activity import get_monthly_history

        ts = current_month_iso()
        with db_module.db() as conn:
            for _ in range(3):
                insert_queue_item(conn, "success", ts)
            conn.commit()

        now = datetime.now(timezone.utc)
        current_key = f"{now.year:04d}-{now.month:02d}"

        with db_module.db() as conn:
            history = get_monthly_history(conn, 6)

        current_entry = next((h for h in history if h["month"] == current_key), None)
        assert current_entry is not None
        assert current_entry["count"] == 3

    def test_respects_limit(self, client):
        """Passing months=2 returns only 2 entries."""
        import src.db as db_module
        from src.utils.activity import get_monthly_history

        with db_module.db() as conn:
            history = get_monthly_history(conn, 2)

        assert len(history) == 2

    def test_chronological_order(self, client):
        """Results are in ascending chronological order."""
        import src.db as db_module
        from src.utils.activity import get_monthly_history

        with db_module.db() as conn:
            history = get_monthly_history(conn, 6)

        months = [h["month"] for h in history]
        assert months == sorted(months)

    def test_december_january_boundary(self, client):
        """History spanning Dec->Jan groups correctly across year boundary."""
        import src.db as db_module
        from src.utils.activity import get_monthly_history

        # Insert uploads in Dec 2025 and Jan 2026
        dec_ts = datetime(2025, 12, 20, 12, 0, 0, tzinfo=timezone.utc).isoformat()
        jan_ts = datetime(2026, 1, 10, 12, 0, 0, tzinfo=timezone.utc).isoformat()

        with db_module.db() as conn:
            for _ in range(4):
                insert_queue_item(conn, "success", dec_ts)
            for _ in range(2):
                insert_queue_item(conn, "success", jan_ts)
            conn.commit()

        # Fake "now" to Feb 2026 so that a 3-month window covers Dec, Jan, Feb.
        fake_now = datetime(2026, 2, 5, 10, 0, 0, tzinfo=timezone.utc)
        real_datetime = datetime

        class FakeDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return fake_now

        with patch("src.utils.activity.datetime", FakeDatetime):
            with db_module.db() as conn:
                history = get_monthly_history(conn, 3)

        assert len(history) == 3

        month_map = {h["month"]: h["count"] for h in history}
        assert month_map["2025-12"] == 4
        assert month_map["2026-01"] == 2
        assert month_map["2026-02"] == 0

        # Verify ordering crosses the year boundary correctly
        months = [h["month"] for h in history]
        assert months == ["2025-12", "2026-01", "2026-02"]


# --------------------------------------------------------------------------
# TestPaceEstimate
# --------------------------------------------------------------------------

class TestPaceEstimate:
    def test_no_data_returns_none(self, client):
        """No recent uploads returns None."""
        import src.db as db_module
        from src.utils.activity import estimate_pace

        with db_module.db() as conn:
            pace = estimate_pace(conn)

        assert pace is None

    def test_with_recent_uploads(self, client):
        """Recent uploads return a float."""
        import src.db as db_module
        from src.utils.activity import estimate_pace

        # Insert items from 3 days ago
        three_days_ago = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
        with db_module.db() as conn:
            for _ in range(6):
                insert_queue_item(conn, "success", three_days_ago)
            conn.commit()

        with db_module.db() as conn:
            pace = estimate_pace(conn)

        assert pace is not None
        assert isinstance(pace, float)
        assert pace > 0


# --------------------------------------------------------------------------
# TestActivityAPI
# --------------------------------------------------------------------------

class TestActivityAPI:
    def test_health_200(self, client):
        """GET /api/activity/health returns 200."""
        response = client.get("/api/activity/health")
        assert response.status_code == 200

    def test_health_json_structure(self, client):
        """Health response has expected fields."""
        response = client.get("/api/activity/health")
        data = response.get_json()
        assert "uploads" in data
        assert "queued" in data
        assert "minimum" in data
        assert "projected" in data
        assert "needed" in data
        assert "critical" in data
        assert "enforce" in data
        assert "days_remaining" in data
        assert "pace" in data

    def test_history_200(self, client):
        """GET /api/activity/history returns 200."""
        response = client.get("/api/activity/history")
        assert response.status_code == 200

    def test_history_default_6_months(self, client):
        """Default history returns 6 entries."""
        response = client.get("/api/activity/history")
        data = response.get_json()
        assert len(data) == 6

    def test_history_custom_months(self, client):
        """Custom months parameter works."""
        response = client.get("/api/activity/history?months=3")
        data = response.get_json()
        assert len(data) == 3

    def test_history_invalid_months_clamped(self, client):
        """Invalid months parameter is clamped."""
        response = client.get("/api/activity/history?months=0")
        data = response.get_json()
        assert len(data) == 1

        response = client.get("/api/activity/history?months=100")
        data = response.get_json()
        assert len(data) == 24


# --------------------------------------------------------------------------
# TestActivityCLI
# --------------------------------------------------------------------------

class TestActivityCLI:
    def test_json_output(self, client):
        """CLI with --json outputs valid JSON."""
        from src.cli import main
        import io
        import sys

        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            main(["--json", "activity"])
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        data = json.loads(output)
        assert "uploads" in data
        assert "critical" in data

    def test_human_output(self, client):
        """CLI without --json outputs human-readable text."""
        from src.cli import main
        import io
        import sys

        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            main(["activity"])
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        assert "Uploads this month:" in output
        assert "Projected:" in output

    def test_warning_when_critical(self, client):
        """CLI shows WARNING when critical."""
        from src.cli import main
        import io
        import sys

        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            main(["activity"])
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        assert "WARNING" in output


# --------------------------------------------------------------------------
# TestNtfy
# --------------------------------------------------------------------------

class TestNtfy:
    def test_transition_sends(self, client):
        """Notification is sent on False->True transition."""
        import src.db as db_module
        from src.utils.activity import check_and_notify_critical, send_ntfy

        with db_module.db() as conn:
            db_module.set_setting(conn, "ntfy_enabled", "1")
            db_module.set_setting(conn, "ntfy_url", "https://ntfy.example.com")
            db_module.set_setting(conn, "ntfy_topic", "test-topic")
            db_module.set_setting(conn, "tl_last_critical_state", "0")
            conn.commit()

        with patch("src.utils.activity.send_ntfy", return_value=True) as mock_send:
            with db_module.db() as conn:
                check_and_notify_critical(conn, True)

            mock_send.assert_called_once()

    def test_already_critical_skips(self, client):
        """No notification when already in critical state."""
        import src.db as db_module
        from src.utils.activity import check_and_notify_critical

        with db_module.db() as conn:
            db_module.set_setting(conn, "ntfy_enabled", "1")
            db_module.set_setting(conn, "ntfy_url", "https://ntfy.example.com")
            db_module.set_setting(conn, "ntfy_topic", "test-topic")
            db_module.set_setting(conn, "tl_last_critical_state", "1")
            conn.commit()

        with patch("src.utils.activity.send_ntfy") as mock_send:
            with db_module.db() as conn:
                check_and_notify_critical(conn, True)

            mock_send.assert_not_called()

    def test_disabled_skips(self, client):
        """No notification when ntfy is disabled."""
        import src.db as db_module
        from src.utils.activity import check_and_notify_critical

        with db_module.db() as conn:
            db_module.set_setting(conn, "ntfy_enabled", "0")
            db_module.set_setting(conn, "tl_last_critical_state", "0")
            conn.commit()

        with patch("src.utils.activity.send_ntfy") as mock_send:
            with db_module.db() as conn:
                check_and_notify_critical(conn, True)

            mock_send.assert_not_called()

    def test_empty_url_topic_skips(self):
        """send_ntfy returns False when url or topic is empty."""
        from src.utils.activity import send_ntfy

        assert send_ntfy("", "topic", "Title", "msg") is False
        assert send_ntfy("https://ntfy.sh", "", "Title", "msg") is False

    def test_invalid_url_scheme_rejected(self):
        """send_ntfy rejects URLs without http/https scheme."""
        from src.utils.activity import send_ntfy

        assert send_ntfy("ftp://evil.com", "topic", "Title", "msg") is False
        assert send_ntfy("javascript:alert(1)", "topic", "Title", "msg") is False

    def test_invalid_topic_rejected(self):
        """send_ntfy rejects topics with special characters."""
        from src.utils.activity import send_ntfy

        with patch("src.utils.activity.httpx.post") as mock_post:
            assert send_ntfy("https://ntfy.sh", "../etc/passwd", "Title", "msg") is False
            assert send_ntfy("https://ntfy.sh", "topic with spaces", "Title", "msg") is False
            mock_post.assert_not_called()

    def test_network_error_handled(self):
        """send_ntfy handles network errors gracefully."""
        from src.utils.activity import send_ntfy

        with patch("src.utils.activity.httpx.post", side_effect=Exception("connection failed")):
            result = send_ntfy("https://ntfy.example.com", "topic", "Title", "msg")
            assert result is False

    def test_state_updates_on_recovery(self, client):
        """State updates to 0 when critical becomes False."""
        import src.db as db_module
        from src.utils.activity import check_and_notify_critical

        with db_module.db() as conn:
            db_module.set_setting(conn, "ntfy_enabled", "1")
            db_module.set_setting(conn, "ntfy_url", "https://ntfy.example.com")
            db_module.set_setting(conn, "ntfy_topic", "test-topic")
            db_module.set_setting(conn, "tl_last_critical_state", "1")
            conn.commit()

        with patch("src.utils.activity.send_ntfy"):
            with db_module.db() as conn:
                check_and_notify_critical(conn, False)

        with db_module.db() as conn:
            state = db_module.get_setting(conn, "tl_last_critical_state")
        assert state == "0"
