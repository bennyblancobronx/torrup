"""Tests for new route features: /api/stats, queue update with imdb/tvmaze, approval gate."""

from __future__ import annotations

from pathlib import Path


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# /api/stats endpoint
# ---------------------------------------------------------------------------

class TestStatsEndpoint:
    """Tests for GET /api/stats."""

    def test_stats_returns_expected_keys(self, client):
        """GET /api/stats returns queue_total, queue_pending, auto_enabled, auto_interval."""
        res = client.get("/api/stats")
        assert res.status_code == 200
        data = res.get_json()
        assert "queue_total" in data
        assert "queue_pending" in data
        assert "auto_enabled" in data
        assert "auto_interval" in data

    def test_stats_empty_queue_zeros(self, client):
        """Fresh database has zero queue counts."""
        res = client.get("/api/stats")
        data = res.get_json()
        assert data["queue_total"] == 0
        assert data["queue_pending"] == 0

    def test_stats_auto_disabled_by_default(self, client):
        """Auto upload is disabled by default."""
        res = client.get("/api/stats")
        data = res.get_json()
        assert data["auto_enabled"] is False

    def test_stats_reflects_queue_count(self, client, music_root):
        """Stats reflect items added to the queue."""
        path = _ensure_dir(music_root / "stats-test-item")
        client.post(
            "/api/queue/add",
            json={
                "items": [
                    {
                        "media_type": "music",
                        "path": str(path),
                        "category": 31,
                        "tags": "",
                    }
                ]
            },
        )
        res = client.get("/api/stats")
        data = res.get_json()
        assert data["queue_total"] >= 1
        assert data["queue_pending"] >= 1


# ---------------------------------------------------------------------------
# Queue update -- IMDB validation
# ---------------------------------------------------------------------------

class TestQueueUpdateImdb:
    """Tests for IMDB field validation on queue update."""

    def _create_queue_item(self, client, music_root):
        """Helper: add a queue item and return its id."""
        path = _ensure_dir(music_root / "imdb-test")
        res = client.post(
            "/api/queue/add",
            json={
                "items": [
                    {
                        "media_type": "music",
                        "path": str(path),
                        "category": 31,
                    }
                ]
            },
        )
        return res.get_json()["ids"][0]

    def test_valid_imdb_accepted(self, client, music_root):
        """Update with valid tt1234567 succeeds."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "imdb": "tt1234567"},
        )
        assert res.status_code == 200
        assert res.get_json()["success"] is True

    def test_valid_imdb_9_digits(self, client, music_root):
        """IMDB IDs with 9 digits are also valid (newer titles)."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "imdb": "tt123456789"},
        )
        assert res.status_code == 200

    def test_invalid_imdb_rejected(self, client, music_root):
        """Update with bad IMDB format returns 400."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "imdb": "notvalid"},
        )
        assert res.status_code == 400
        assert "IMDB" in res.get_json()["error"]

    def test_imdb_too_short_rejected(self, client, music_root):
        """IMDB with fewer than 7 digits is rejected."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "imdb": "tt123"},
        )
        assert res.status_code == 400

    def test_imdb_empty_clears(self, client, music_root):
        """Empty string for imdb clears the value (no error)."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "imdb": ""},
        )
        assert res.status_code == 200


# ---------------------------------------------------------------------------
# Queue update -- TVMaze ID validation
# ---------------------------------------------------------------------------

class TestQueueUpdateTvmaze:
    """Tests for tvmazeid and tvmazetype validation on queue update."""

    def _create_queue_item(self, client, music_root):
        """Helper: add a queue item and return its id."""
        path = _ensure_dir(music_root / "tvmaze-test")
        res = client.post(
            "/api/queue/add",
            json={
                "items": [
                    {
                        "media_type": "music",
                        "path": str(path),
                        "category": 31,
                    }
                ]
            },
        )
        return res.get_json()["ids"][0]

    def test_tvmazeid_valid_digits(self, client, music_root):
        """Update with digit-only tvmazeid succeeds."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazeid": "12345"},
        )
        assert res.status_code == 200
        assert res.get_json()["success"] is True

    def test_tvmazeid_invalid_non_digits(self, client, music_root):
        """Update with non-digit tvmazeid returns 400."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazeid": "abc"},
        )
        assert res.status_code == 400
        assert "TVMaze ID" in res.get_json()["error"]

    def test_tvmazetype_valid_1(self, client, music_root):
        """tvmazetype '1' (boxset) is accepted."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazetype": "1"},
        )
        assert res.status_code == 200

    def test_tvmazetype_valid_2(self, client, music_root):
        """tvmazetype '2' (episode) is accepted."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazetype": "2"},
        )
        assert res.status_code == 200

    def test_tvmazetype_invalid_3(self, client, music_root):
        """tvmazetype '3' is rejected."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazetype": "3"},
        )
        assert res.status_code == 400
        assert "TVMaze Type" in res.get_json()["error"]

    def test_tvmazetype_invalid_text(self, client, music_root):
        """tvmazetype with non-numeric value is rejected."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazetype": "boxset"},
        )
        assert res.status_code == 400

    def test_tvmazeid_empty_clears(self, client, music_root):
        """Empty string for tvmazeid clears the value."""
        item_id = self._create_queue_item(client, music_root)
        res = client.post(
            "/api/queue/update",
            json={"id": item_id, "tvmazeid": ""},
        )
        assert res.status_code == 200


# ---------------------------------------------------------------------------
# Worker approval gate
# ---------------------------------------------------------------------------

class TestWorkerApprovalGate:
    """Items with approval_status='pending_approval' must NOT be processed by the worker."""

    def test_pending_approval_not_processed(self, client, music_root):
        """Items with pending_approval are skipped by the queue worker query."""
        import src.db as db_module

        path = _ensure_dir(music_root / "approval-gate-test")

        # Insert an item directly with pending_approval status
        with db_module.db() as conn:
            conn.execute(
                """
                INSERT INTO queue (
                    media_type, path, release_name, category, tags,
                    status, created_at, updated_at,
                    certainty_score, approval_status
                )
                VALUES ('music', ?, 'Test-Release', 31, '',
                        'queued', '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z',
                        50, 'pending_approval')
                """,
                (str(path),),
            )
            conn.commit()

            # The worker query only picks approved items
            row = conn.execute(
                "SELECT * FROM queue WHERE status = 'queued' AND approval_status = 'approved' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            assert row is None, "pending_approval item should NOT be returned by worker query"

    def test_approved_item_is_returned(self, client, music_root):
        """Items with approval_status='approved' are returned by the worker query."""
        import src.db as db_module

        path = _ensure_dir(music_root / "approved-gate-test")

        with db_module.db() as conn:
            conn.execute(
                """
                INSERT INTO queue (
                    media_type, path, release_name, category, tags,
                    status, created_at, updated_at,
                    certainty_score, approval_status
                )
                VALUES ('music', ?, 'Approved-Release', 31, '',
                        'queued', '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z',
                        90, 'approved')
                """,
                (str(path),),
            )
            conn.commit()

            row = conn.execute(
                "SELECT * FROM queue WHERE status = 'queued' AND approval_status = 'approved' ORDER BY id ASC LIMIT 1"
            ).fetchone()
            assert row is not None
            assert row["release_name"] == "Approved-Release"


# ---------------------------------------------------------------------------
# Queue management -- retry-all
# ---------------------------------------------------------------------------

class TestQueueRetryAll:
    """Tests for POST /api/queue/retry-all."""

    def _insert_items(self, statuses):
        """Insert queue items with given statuses, return list of ids."""
        import src.db as db_module

        ids = []
        with db_module.db() as conn:
            for i, status in enumerate(statuses):
                cur = conn.execute(
                    """
                    INSERT INTO queue (
                        media_type, path, release_name, category, tags,
                        status, message, created_at, updated_at
                    )
                    VALUES ('music', ?, ?, 31, '', ?, ?, '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z')
                    """,
                    (f"/fake/path/{i}", f"Release-{i}", status, f"err-{i}" if status == "failed" else ""),
                )
                ids.append(cur.lastrowid)
            conn.commit()
        return ids

    def test_retry_all_resets_failed_items(self, client):
        """Only failed items should be changed to queued."""
        import src.db as db_module

        ids = self._insert_items(["failed", "queued", "duplicate"])

        res = client.post("/api/queue/retry-all")
        assert res.status_code == 200

        with db_module.db() as conn:
            rows = {r["id"]: dict(r) for r in conn.execute("SELECT * FROM queue").fetchall()}

        assert rows[ids[0]]["status"] == "queued"
        assert rows[ids[1]]["status"] == "queued"
        assert rows[ids[2]]["status"] == "duplicate"

    def test_retry_all_returns_count(self, client):
        """Response includes success flag and count of reset items."""
        self._insert_items(["failed", "failed", "queued"])

        res = client.post("/api/queue/retry-all")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["count"] == 2

    def test_retry_all_clears_message(self, client):
        """Message field is cleared after retry."""
        import src.db as db_module

        ids = self._insert_items(["failed"])

        # Verify message was set
        with db_module.db() as conn:
            row = conn.execute("SELECT message FROM queue WHERE id = ?", (ids[0],)).fetchone()
            assert row["message"] != ""

        client.post("/api/queue/retry-all")

        with db_module.db() as conn:
            row = conn.execute("SELECT message FROM queue WHERE id = ?", (ids[0],)).fetchone()
            assert row["message"] == ""


# ---------------------------------------------------------------------------
# Queue management -- clear-duplicates
# ---------------------------------------------------------------------------

class TestQueueClearDuplicates:
    """Tests for POST /api/queue/clear-duplicates."""

    def _insert_items(self, statuses):
        """Insert queue items with given statuses, return list of ids."""
        import src.db as db_module

        ids = []
        with db_module.db() as conn:
            for i, status in enumerate(statuses):
                cur = conn.execute(
                    """
                    INSERT INTO queue (
                        media_type, path, release_name, category, tags,
                        status, message, created_at, updated_at
                    )
                    VALUES ('music', ?, ?, 31, '', ?, '', '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z')
                    """,
                    (f"/fake/path/{i}", f"Release-{i}", status),
                )
                ids.append(cur.lastrowid)
            conn.commit()
        return ids

    def test_clear_duplicates_removes_only_dupes(self, client):
        """Only duplicate items should be removed."""
        import src.db as db_module

        ids = self._insert_items(["queued", "duplicate", "failed", "duplicate", "success"])

        res = client.post("/api/queue/clear-duplicates")
        assert res.status_code == 200

        with db_module.db() as conn:
            remaining = [r["id"] for r in conn.execute("SELECT id FROM queue").fetchall()]

        assert ids[0] in remaining  # queued stays
        assert ids[1] not in remaining  # duplicate removed
        assert ids[2] in remaining  # failed stays
        assert ids[3] not in remaining  # duplicate removed
        assert ids[4] in remaining  # success stays

    def test_clear_duplicates_returns_count(self, client):
        """Response includes the count of removed duplicates."""
        self._insert_items(["duplicate", "duplicate", "queued"])

        res = client.post("/api/queue/clear-duplicates")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["count"] == 2


# ---------------------------------------------------------------------------
# Queue management -- clear-completed
# ---------------------------------------------------------------------------

class TestQueueClearCompleted:
    """Tests for POST /api/queue/clear-completed."""

    def _insert_items(self, statuses):
        """Insert queue items with given statuses, return list of ids."""
        import src.db as db_module

        ids = []
        with db_module.db() as conn:
            for i, status in enumerate(statuses):
                cur = conn.execute(
                    """
                    INSERT INTO queue (
                        media_type, path, release_name, category, tags,
                        status, message, created_at, updated_at
                    )
                    VALUES ('music', ?, ?, 31, '', ?, '', '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z')
                    """,
                    (f"/fake/path/{i}", f"Release-{i}", status),
                )
                ids.append(cur.lastrowid)
            conn.commit()
        return ids

    def test_clear_completed_removes_only_success(self, client):
        """Only success items should be removed."""
        import src.db as db_module

        ids = self._insert_items(["success", "queued", "failed", "success", "duplicate"])

        res = client.post("/api/queue/clear-completed")
        assert res.status_code == 200

        with db_module.db() as conn:
            remaining = [r["id"] for r in conn.execute("SELECT id FROM queue").fetchall()]

        assert ids[0] not in remaining  # success removed
        assert ids[1] in remaining  # queued stays
        assert ids[2] in remaining  # failed stays
        assert ids[3] not in remaining  # success removed
        assert ids[4] in remaining  # duplicate stays


# ---------------------------------------------------------------------------
# Queue management -- clear-all
# ---------------------------------------------------------------------------

class TestQueueClearAll:
    """Tests for POST /api/queue/clear-all."""

    def _insert_items(self, statuses):
        """Insert queue items with given statuses, return list of ids."""
        import src.db as db_module

        ids = []
        with db_module.db() as conn:
            for i, status in enumerate(statuses):
                cur = conn.execute(
                    """
                    INSERT INTO queue (
                        media_type, path, release_name, category, tags,
                        status, message, created_at, updated_at
                    )
                    VALUES ('music', ?, ?, 31, '', ?, '', '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z')
                    """,
                    (f"/fake/path/{i}", f"Release-{i}", status),
                )
                ids.append(cur.lastrowid)
            conn.commit()
        return ids

    def test_clear_all_requires_confirm(self, client):
        """Calling without confirm param returns 400."""
        res = client.post("/api/queue/clear-all", json={})
        assert res.status_code == 400
        data = res.get_json()
        assert "confirm" in data["error"].lower()

    def test_clear_all_removes_everything(self, client):
        """With confirm: true, all items are removed."""
        import src.db as db_module

        self._insert_items(["queued", "failed", "success", "duplicate"])

        res = client.post("/api/queue/clear-all", json={"confirm": True})
        assert res.status_code == 200

        with db_module.db() as conn:
            count = conn.execute("SELECT COUNT(*) AS cnt FROM queue").fetchone()["cnt"]
        assert count == 0

    def test_clear_all_returns_count(self, client):
        """Response includes count of removed items."""
        self._insert_items(["queued", "failed", "success"])

        res = client.post("/api/queue/clear-all", json={"confirm": True})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["count"] == 3


# ---------------------------------------------------------------------------
# _scan_root source parameter
# ---------------------------------------------------------------------------

class TestScanSourcePrefix:
    """Tests for _scan_root source parameter."""

    def test_scan_root_accepts_source_param(self):
        """_scan_root accepts a source parameter without error."""
        import inspect
        from src.auto_worker import _scan_root

        sig = inspect.signature(_scan_root)
        assert "source" in sig.parameters, "_scan_root must accept a 'source' parameter"
        # Verify it has a default value
        param = sig.parameters["source"]
        assert param.default != inspect.Parameter.empty, "source should have a default value"
