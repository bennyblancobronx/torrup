"""Pytest fixtures for Torrup tests."""

import importlib
import os

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Create a Flask test client with fresh database."""
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("TORRUP_DB_PATH", str(tmp_path / "torrup.db"))
    monkeypatch.setenv("TORRUP_OUTPUT_DIR", str(tmp_path / "output"))
    monkeypatch.setenv("TORRUP_RUN_WORKER", "0")

    import src.config as config
    import src.db as db
    import app as app_module

    importlib.reload(config)
    importlib.reload(db)
    importlib.reload(app_module)

    app = app_module.app
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def media_dir(tmp_path):
    """Create a temporary media directory structure for browse tests."""
    music_dir = tmp_path / "media" / "music"
    music_dir.mkdir(parents=True)

    # Create some test files
    album_dir = music_dir / "Artist-Album-2024-FLAC"
    album_dir.mkdir()
    (album_dir / "01-track.flac").write_bytes(b"\x00" * 1024)
    (album_dir / "02-track.flac").write_bytes(b"\x00" * 1024)

    return tmp_path / "media"


@pytest.fixture()
def mock_api_key(monkeypatch):
    """Set a mock API key for API tests."""
    monkeypatch.setenv("TL_ANNOUNCE_KEY", "test-announce-key-12345")


@pytest.fixture()
def queue_item_data():
    """Return valid queue item data for testing."""
    return {
        "items": [
            {
                "media_type": "music",
                "path": "/tmp/test-item",
                "category": 31,
                "tags": "rock,indie",
            }
        ]
    }
