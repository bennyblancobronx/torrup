"""Tests for background worker in src/worker.py."""

import importlib
import os
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture()
def worker_db(tmp_path, monkeypatch):
    """Create a fresh database for worker tests."""
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("TORRUP_DB_PATH", str(tmp_path / "torrup.db"))
    monkeypatch.setenv("TORRUP_OUTPUT_DIR", str(tmp_path / "output"))
    monkeypatch.setenv("TORRUP_RUN_WORKER", "0")

    import src.config as config
    import src.db as db_module

    importlib.reload(config)
    importlib.reload(db_module)

    db_module.init_db()
    return db_module


class TestSanitizeErrorMessage:
    """Tests for sanitize_error_message function."""

    def test_sanitize_removes_file_paths(self):
        """Verify file paths are redacted."""
        from src.worker import sanitize_error_message

        error = Exception("Cannot open /home/user/secret/file.txt")
        result = sanitize_error_message(error)
        assert "/home/user/secret/file.txt" not in result
        assert "[path]" in result

    def test_sanitize_removes_secrets(self):
        """Verify secrets are redacted."""
        from src.worker import sanitize_error_message

        error = Exception("API key=abc123secret failed")
        result = sanitize_error_message(error)
        assert "abc123secret" not in result
        assert "[redacted]" in result

    def test_sanitize_removes_tokens(self):
        """Verify tokens are redacted."""
        from src.worker import sanitize_error_message

        error = Exception("token: my-secret-token-value invalid")
        result = sanitize_error_message(error)
        assert "my-secret-token-value" not in result

    def test_sanitize_truncates_long_messages(self):
        """Verify long messages are truncated."""
        from src.worker import sanitize_error_message

        error = Exception("x" * 500)
        result = sanitize_error_message(error)
        assert len(result) <= 203  # 200 + "..."


class TestUpdateQueueStatus:
    """Tests for update_queue_status function."""

    def test_update_queue_status_changes_status(self, worker_db):
        """Verify status is updated in database."""
        from src.worker import update_queue_status
        from src.utils import now_iso

        with worker_db.db() as conn:
            # Insert a test item
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", "/tmp/test", "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Update status
            update_queue_status(conn, item_id, "preparing", "Processing...")
            conn.commit()

            # Verify
            row = conn.execute(
                "SELECT status, message FROM queue WHERE id = ?", (item_id,)
            ).fetchone()
            assert row["status"] == "preparing"
            assert row["message"] == "Processing..."


class TestProcessQueueItem:
    """Tests for process_queue_item function."""

    @patch("src.worker.check_exists")
    @patch("src.worker.upload_torrent")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    @patch("src.worker.write_xml_metadata")
    def test_process_queue_item_path_not_found(
        self,
        mock_xml,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_upload,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify item fails when path not found."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", "/nonexistent/path", "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify failed status
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "failed"
            assert "not found" in row["message"].lower()

    @patch("src.worker.check_exists")
    @patch("src.worker.upload_torrent")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    @patch("src.worker.write_xml_metadata")
    def test_process_queue_item_duplicate(
        self,
        mock_xml,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_upload,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify item is marked duplicate when already exists."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        # Create a test directory
        test_dir = tmp_path / "test-album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        mock_exists.return_value = True  # Release exists on TL

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", str(test_dir), "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify duplicate status
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "duplicate"

    @patch("src.worker.check_exists")
    @patch("src.worker.upload_torrent")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    @patch("src.worker.write_xml_metadata")
    def test_process_queue_item_upload_success(
        self,
        mock_xml,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_upload,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify successful upload flow."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        # Create a test directory
        test_dir = tmp_path / "test-album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        # Setup mocks
        mock_exists.return_value = False
        mock_meta.return_value = {"artist": "Test Artist"}
        mock_thumb.return_value = None
        mock_nfo.return_value = tmp_path / "test.nfo"
        mock_torrent.return_value = tmp_path / "test.torrent"
        mock_xml.return_value = tmp_path / "test.xml"
        mock_upload.return_value = {"success": True, "torrent_id": 12345}

        (tmp_path / "test.nfo").touch()
        (tmp_path / "test.torrent").touch()
        (tmp_path / "test.xml").touch()

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", str(test_dir), "Test-Release", 31, "rock", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify success status
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "success"
            assert "12345" in row["message"]

    @patch("src.worker.check_exists")
    @patch("src.worker.upload_torrent")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    @patch("src.worker.write_xml_metadata")
    def test_process_queue_item_upload_failure(
        self,
        mock_xml,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_upload,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify failed upload is handled."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        # Create a test directory
        test_dir = tmp_path / "test-album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        # Setup mocks
        mock_exists.return_value = False
        mock_meta.return_value = {}
        mock_thumb.return_value = None
        mock_nfo.return_value = tmp_path / "test.nfo"
        mock_torrent.return_value = tmp_path / "test.torrent"
        mock_xml.return_value = tmp_path / "test.xml"
        mock_upload.return_value = {"success": False, "error": "Upload rejected"}

        (tmp_path / "test.nfo").touch()
        (tmp_path / "test.torrent").touch()
        (tmp_path / "test.xml").touch()

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", str(test_dir), "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify failed status
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "failed"
            assert "rejected" in row["message"].lower()

    @patch("src.worker.check_exists")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    def test_process_queue_item_prepare_exception(
        self,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify exception during prepare is handled."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        # Create a test directory
        test_dir = tmp_path / "test-album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        # Setup mocks
        mock_exists.return_value = False
        mock_meta.return_value = {}
        mock_thumb.return_value = None
        mock_nfo.side_effect = Exception("NFO generation failed")

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", str(test_dir), "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify failed status
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "failed"
            assert "Prepare failed" in row["message"]

    @patch("src.worker.check_exists")
    @patch("src.worker.upload_torrent")
    @patch("src.worker.create_torrent")
    @patch("src.worker.generate_nfo")
    @patch("src.worker.extract_metadata")
    @patch("src.worker.extract_thumbnail")
    @patch("src.worker.write_xml_metadata")
    def test_process_queue_item_upload_exception(
        self,
        mock_xml,
        mock_thumb,
        mock_meta,
        mock_nfo,
        mock_torrent,
        mock_upload,
        mock_exists,
        worker_db,
        tmp_path,
    ):
        """Verify exception during upload is handled."""
        from src.worker import process_queue_item
        from src.utils import now_iso

        # Create a test directory
        test_dir = tmp_path / "test-album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        # Setup mocks
        mock_exists.return_value = False
        mock_meta.return_value = {}
        mock_thumb.return_value = None
        mock_nfo.return_value = tmp_path / "test.nfo"
        mock_torrent.return_value = tmp_path / "test.torrent"
        mock_xml.return_value = tmp_path / "test.xml"
        mock_upload.side_effect = Exception("Network error during upload")

        (tmp_path / "test.nfo").touch()
        (tmp_path / "test.torrent").touch()
        (tmp_path / "test.xml").touch()

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", str(test_dir), "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()
            item_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
            process_queue_item(conn, row)

            # Verify failed status with upload error
            row = conn.execute("SELECT status, message FROM queue WHERE id = ?", (item_id,)).fetchone()
            assert row["status"] == "failed"
            assert "Upload error" in row["message"]


class TestQueueWorker:
    """Tests for queue_worker function."""

    @patch("src.worker.time.sleep")
    @patch("src.worker.process_queue_item")
    def test_queue_worker_processes_queued_item(
        self,
        mock_process,
        mock_sleep,
        worker_db,
        tmp_path,
    ):
        """Verify queue worker processes queued items."""
        from src.worker import queue_worker
        from src.utils import now_iso

        # Make sleep raise exception to stop the loop after first iteration
        call_count = [0]
        def stop_loop(*args):
            call_count[0] += 1
            if call_count[0] >= 2:
                raise KeyboardInterrupt("Stop test")

        mock_sleep.side_effect = stop_loop

        with worker_db.db() as conn:
            now = now_iso()
            conn.execute(
                """
                INSERT INTO queue (media_type, path, release_name, category, tags, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("music", "/tmp/test", "Test-Release", 31, "", "queued", now, now),
            )
            conn.commit()

        try:
            queue_worker()
        except KeyboardInterrupt:
            pass

        # Verify process_queue_item was called
        assert mock_process.called

    @patch("src.worker.time.sleep")
    @patch("src.worker.process_queue_item")
    def test_queue_worker_sleeps_when_no_items(
        self,
        mock_process,
        mock_sleep,
        worker_db,
    ):
        """Verify queue worker sleeps when no queued items."""
        from src.worker import queue_worker

        # Make sleep raise exception to stop the loop after first iteration
        call_count = [0]
        def stop_loop(*args):
            call_count[0] += 1
            if call_count[0] >= 1:
                raise KeyboardInterrupt("Stop test")

        mock_sleep.side_effect = stop_loop

        try:
            queue_worker()
        except KeyboardInterrupt:
            pass

        # Verify sleep was called but process was not
        assert mock_sleep.called
        assert not mock_process.called
