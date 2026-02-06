"""Tests for TorrentLeech API client in src/api.py."""

import os
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")


class TestCheckExists:
    """Tests for check_exists function."""

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_found(self, mock_post):
        """Verify check_exists returns True when release exists."""
        from src.api import check_exists

        mock_response = MagicMock()
        mock_response.text = "1"
        mock_post.return_value = mock_response

        result = check_exists("Test.Release.Name")

        assert result is True
        mock_post.assert_called_once()

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_not_found(self, mock_post):
        """Verify check_exists returns False when release not found."""
        from src.api import check_exists

        mock_response = MagicMock()
        mock_response.text = "0"
        mock_post.return_value = mock_response

        result = check_exists("Nonexistent.Release")

        assert result is False

    @patch("src.api.ANNOUNCE_KEY", "")
    def test_check_exists_no_key(self):
        """Verify check_exists returns False when no API key."""
        from src.api import check_exists

        result = check_exists("Any.Release")
        assert result is False

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_handles_exception(self, mock_post):
        """Verify check_exists returns False on network error."""
        from src.api import check_exists

        mock_post.side_effect = Exception("Network error")

        result = check_exists("Test.Release")
        assert result is False

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_handles_quotes(self, mock_post):
        """Verify check_exists handles quoted "1" or "0"."""
        from src.api import check_exists

        mock_response = MagicMock()
        mock_response.text = '"1"'
        mock_post.return_value = mock_response

        assert check_exists("Quoted.Release") is True

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_fuzzy(self, mock_post):
        """Verify check_exists sends exact=0 for fuzzy search."""
        from src.api import check_exists

        mock_response = MagicMock()
        mock_response.text = "0"
        mock_post.return_value = mock_response

        check_exists("Fuzzy.Release", exact=False)

        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["data"]["exact"] == "0"

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_check_exists_sends_correct_data(self, mock_post):
        """Verify check_exists sends correct search parameters."""
        from src.api import check_exists

        mock_response = MagicMock()
        mock_response.text = "0"
        mock_post.return_value = mock_response

        check_exists("Artist.Album.2024.FLAC")

        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["data"]["exact"] == "1"
        assert "Artist.Album.2024.FLAC" in call_kwargs[1]["data"]["query"]


class TestUploadTorrent:
    """Tests for upload_torrent function."""

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    @patch("builtins.open", mock_open(read_data=b"torrent data"))
    def test_upload_torrent_success(self, mock_post, tmp_path):
        """Verify upload_torrent returns success on valid response."""
        from src.api import upload_torrent

        mock_response = MagicMock()
        mock_response.text = "12345"  # Valid torrent ID
        mock_post.return_value = mock_response

        torrent_path = tmp_path / "test.torrent"
        nfo_path = tmp_path / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        result = upload_torrent(torrent_path, nfo_path, 31, "tag1,tag2")

        assert result["success"] is True
        assert result["torrent_id"] == 12345

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    @patch("builtins.open", mock_open(read_data=b"torrent data"))
    def test_upload_torrent_failure(self, mock_post, tmp_path):
        """Verify upload_torrent returns failure on error response."""
        from src.api import upload_torrent

        mock_response = MagicMock()
        mock_response.text = "Error: Duplicate torrent"  # Not a valid ID
        mock_post.return_value = mock_response

        torrent_path = tmp_path / "test.torrent"
        nfo_path = tmp_path / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        result = upload_torrent(torrent_path, nfo_path, 31, "")

        assert result["success"] is False
        assert "error" in result
        assert "Duplicate" in result["error"]

    @patch("src.api.ANNOUNCE_KEY", "")
    def test_upload_torrent_no_key(self, tmp_path):
        """Verify upload_torrent raises exception when no API key."""
        from src.api import upload_torrent

        torrent_path = tmp_path / "test.torrent"
        nfo_path = tmp_path / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        with pytest.raises(Exception) as exc_info:
            upload_torrent(torrent_path, nfo_path, 31, "")

        assert "not configured" in str(exc_info.value)

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    @patch("builtins.open", mock_open(read_data=b"data"))
    def test_upload_torrent_sends_correct_data(self, mock_post, tmp_path):
        """Verify upload_torrent sends correct form data."""
        from src.api import upload_torrent

        mock_response = MagicMock()
        mock_response.text = "99999"
        mock_post.return_value = mock_response

        torrent_path = tmp_path / "release.torrent"
        nfo_path = tmp_path / "release.nfo"
        torrent_path.touch()
        nfo_path.touch()

        upload_torrent(torrent_path, nfo_path, 31, "rock,indie")

        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["data"]["category"] == "31"
        assert call_kwargs[1]["data"]["tags"] == "rock,indie"
        assert "torrent" in call_kwargs[1]["files"]
        assert "nfo" in call_kwargs[1]["files"]


class TestDownloadTorrent:
    """Tests for download_torrent function."""

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_download_torrent_success(self, mock_post, tmp_path):
        """Verify download_torrent saves file on valid response."""
        from src.api import download_torrent

        # Bencoded torrent starts with 'd', needs to be > 50 bytes
        fake_torrent = b"d8:announce40:https://tracker.example.com/a/key/announce4:infod6:lengthi1024eee"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = fake_torrent
        mock_post.return_value = mock_response

        dest = tmp_path / "downloaded.torrent"
        result = download_torrent(12345, dest)

        assert result is True
        assert dest.exists()
        assert dest.read_bytes() == fake_torrent
        call_data = mock_post.call_args[1]["data"]
        assert call_data["torrentID"] == "12345"
        assert call_data["announcekey"] == "test-key-123"

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_download_torrent_http_error(self, mock_post, tmp_path):
        """Verify download_torrent returns False on HTTP error."""
        from src.api import download_torrent

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        dest = tmp_path / "fail.torrent"
        result = download_torrent(99999, dest)

        assert result is False
        assert not dest.exists()

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_download_torrent_invalid_content(self, mock_post, tmp_path):
        """Verify download_torrent rejects non-torrent response."""
        from src.api import download_torrent

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Error: not found"
        mock_post.return_value = mock_response

        dest = tmp_path / "bad.torrent"
        result = download_torrent(12345, dest)

        assert result is False

    @patch("src.api.ANNOUNCE_KEY", "")
    def test_download_torrent_no_key(self, tmp_path):
        """Verify download_torrent returns False when no API key."""
        from src.api import download_torrent

        dest = tmp_path / "nokey.torrent"
        result = download_torrent(12345, dest)

        assert result is False

    @patch("src.api.ANNOUNCE_KEY", "test-key-123")
    @patch("src.api.httpx.post")
    def test_download_torrent_network_error(self, mock_post, tmp_path):
        """Verify download_torrent handles network exceptions."""
        from src.api import download_torrent

        mock_post.side_effect = Exception("Connection refused")

        dest = tmp_path / "err.torrent"
        result = download_torrent(12345, dest)

        assert result is False
