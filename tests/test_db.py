"""Tests for database operations in src/db.py."""

import importlib
import os
import sqlite3

import pytest


@pytest.fixture()
def db_conn(tmp_path, monkeypatch):
    """Create a fresh database connection for testing."""
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("TORRUP_DB_PATH", str(tmp_path / "torrup.db"))
    monkeypatch.setenv("TORRUP_OUTPUT_DIR", str(tmp_path / "output"))
    monkeypatch.setenv("TORRUP_RUN_WORKER", "0")

    import src.config as config
    import src.db as db_module

    importlib.reload(config)
    importlib.reload(db_module)

    db_module.init_db()

    with db_module.db() as conn:
        yield conn


class TestInitDb:
    """Tests for init_db function."""

    def test_init_db_creates_settings_table(self, db_conn):
        """Verify settings table is created."""
        row = db_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='settings'"
        ).fetchone()
        assert row is not None
        assert row["name"] == "settings"

    def test_init_db_creates_media_roots_table(self, db_conn):
        """Verify media_roots table is created."""
        row = db_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='media_roots'"
        ).fetchone()
        assert row is not None
        assert row["name"] == "media_roots"

    def test_init_db_creates_queue_table(self, db_conn):
        """Verify queue table is created."""
        row = db_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='queue'"
        ).fetchone()
        assert row is not None
        assert row["name"] == "queue"

    def test_init_db_creates_default_settings(self, db_conn):
        """Verify default settings are populated."""
        from src.db import get_setting

        browse_base = get_setting(db_conn, "browse_base")
        assert browse_base == "/volume/media"

        exclude_dirs = get_setting(db_conn, "exclude_dirs")
        assert "torrents" in exclude_dirs

    def test_init_db_creates_media_roots_for_all_types(self, db_conn):
        """Verify media roots are created for all media types."""
        from src.config import MEDIA_TYPES

        rows = db_conn.execute("SELECT media_type FROM media_roots").fetchall()
        media_types = {r["media_type"] for r in rows}

        for mt in MEDIA_TYPES:
            assert mt in media_types


class TestGetSetting:
    """Tests for get_setting function."""

    def test_get_setting_returns_value(self, db_conn):
        """Verify existing setting is returned."""
        from src.db import get_setting

        value = get_setting(db_conn, "browse_base")
        assert value == "/volume/media"

    def test_get_setting_default_for_missing(self, db_conn):
        """Verify empty string returned for missing key."""
        from src.db import get_setting

        value = get_setting(db_conn, "nonexistent_key_xyz")
        assert value == ""


class TestSetSetting:
    """Tests for set_setting function."""

    def test_set_setting_inserts_new(self, db_conn):
        """Verify new setting is inserted."""
        from src.db import get_setting, set_setting

        set_setting(db_conn, "new_test_key", "new_test_value")
        db_conn.commit()

        value = get_setting(db_conn, "new_test_key")
        assert value == "new_test_value"

    def test_set_setting_updates_existing(self, db_conn):
        """Verify existing setting is updated."""
        from src.db import get_setting, set_setting

        set_setting(db_conn, "browse_base", "/updated/path")
        db_conn.commit()

        value = get_setting(db_conn, "browse_base")
        assert value == "/updated/path"


class TestGetMediaRoots:
    """Tests for get_media_roots function."""

    def test_get_media_roots_returns_list(self, db_conn):
        """Verify media roots are returned as a list of dicts."""
        from src.db import get_media_roots

        roots = get_media_roots(db_conn)
        assert isinstance(roots, list)
        assert len(roots) > 0

    def test_get_media_roots_contains_expected_keys(self, db_conn):
        """Verify each media root has expected keys."""
        from src.db import get_media_roots

        roots = get_media_roots(db_conn)
        for root in roots:
            assert "media_type" in root
            assert "path" in root
            assert "enabled" in root
            assert "default_category" in root


class TestGetExcludes:
    """Tests for get_excludes function."""

    def test_get_excludes_returns_list(self, db_conn):
        """Verify excludes are returned as a list."""
        from src.db import get_excludes

        excludes = get_excludes(db_conn)
        assert isinstance(excludes, list)
        assert len(excludes) > 0

    def test_get_excludes_contains_defaults(self, db_conn):
        """Verify default excludes are present."""
        from src.db import get_excludes

        excludes = get_excludes(db_conn)
        assert "torrents" in excludes
        assert "tmp" in excludes


class TestGetOutputDir:
    """Tests for get_output_dir function."""

    def test_get_output_dir_returns_path(self, db_conn):
        """Verify output dir is returned as Path."""
        from pathlib import Path

        from src.db import get_output_dir

        out_dir = get_output_dir(db_conn)
        assert isinstance(out_dir, Path)

    def test_get_output_dir_creates_directory(self, db_conn, tmp_path):
        """Verify output directory is created if missing."""
        from src.db import get_output_dir, set_setting

        new_dir = tmp_path / "new_output_dir"
        set_setting(db_conn, "output_dir", str(new_dir))
        db_conn.commit()

        out_dir = get_output_dir(db_conn)
        assert out_dir.exists()

    def test_get_output_dir_without_connection(self, db_conn, tmp_path):
        """Verify output dir works when conn is None (creates own connection)."""
        from pathlib import Path

        from src.db import get_output_dir

        # Call without connection - should create its own
        out_dir = get_output_dir(None)
        assert isinstance(out_dir, Path)
        assert out_dir.exists()


class TestQueueOperations:
    """Tests for queue table operations via routes."""

    def test_add_queue_item(self, client, music_root):
        """Verify queue item can be added."""
        path = music_root / "test-item"
        path.mkdir(parents=True, exist_ok=True)
        payload = {
            "items": [
                {
                    "media_type": "music",
                    "path": str(path),
                    "category": 31,
                    "tags": "tag1,tag2",
                }
            ]
        }
        res = client.post("/api/queue/add", json=payload)
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["ids"]) == 1

    def test_update_queue_status(self, client, music_root):
        """Verify queue item status can be updated."""
        path = music_root / "test-update-status"
        path.mkdir(parents=True, exist_ok=True)
        # Add item first
        payload = {
            "items": [
                {
                    "media_type": "music",
                    "path": str(path),
                    "category": 31,
                    "tags": "",
                }
            ]
        }
        res = client.post("/api/queue/add", json=payload)
        item_id = res.get_json()["ids"][0]

        # Update status
        update_res = client.post(
            "/api/queue/update",
            json={"id": item_id, "status": "preparing"}
        )
        assert update_res.status_code == 200

        # Verify status changed
        list_res = client.get("/api/queue")
        items = list_res.get_json()
        item = next(i for i in items if i["id"] == item_id)
        assert item["status"] == "preparing"

    def test_delete_queue_item(self, client, music_root):
        """Verify queue item can be deleted."""
        path = music_root / "test-delete"
        path.mkdir(parents=True, exist_ok=True)
        # Add item first
        payload = {
            "items": [
                {
                    "media_type": "music",
                    "path": str(path),
                    "category": 31,
                    "tags": "",
                }
            ]
        }
        res = client.post("/api/queue/add", json=payload)
        item_id = res.get_json()["ids"][0]

        # Delete item
        delete_res = client.post("/api/queue/delete", json={"id": item_id})
        assert delete_res.status_code == 200

        # Verify item is gone
        list_res = client.get("/api/queue")
        items = list_res.get_json()
        assert not any(i["id"] == item_id for i in items)
