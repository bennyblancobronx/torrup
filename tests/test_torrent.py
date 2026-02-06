"""Tests for torrent creation in src/utils/torrent.py."""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")

from src.utils import create_torrent


class TestCreateTorrent:
    """Tests for create_torrent function."""

    @patch("src.utils.torrent.subprocess.run")
    def test_create_torrent_success(self, mock_run, tmp_path):
        """Verify torrent creation succeeds with valid input."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = create_torrent(test_dir, "Test-Release", out_dir)

        assert mock_run.called
        assert result == out_dir / "Test-Release.torrent"

    @patch("src.utils.torrent.subprocess.run")
    def test_create_torrent_mktorrent_failure(self, mock_run, tmp_path):
        """Verify torrent creation handles mktorrent failure."""
        mock_run.return_value = MagicMock(returncode=1, stderr="mktorrent error")

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(Exception) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "mktorrent failed" in str(exc_info.value)

    @patch("src.utils.torrent.subprocess.run")
    def test_create_torrent_timeout(self, mock_run, tmp_path):
        """Verify torrent creation handles timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("mktorrent", 120)

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(Exception) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "timed out" in str(exc_info.value)

    @patch("src.utils.torrent.subprocess.run")
    def test_create_torrent_subprocess_error(self, mock_run, tmp_path):
        """Verify torrent creation handles subprocess error."""
        mock_run.side_effect = subprocess.SubprocessError("Subprocess failed")

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(Exception) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "subprocess error" in str(exc_info.value)

    def test_create_torrent_invalid_path(self, tmp_path, monkeypatch):
        """Verify torrent creation rejects invalid input path."""
        call_count = [0]

        def mock_validate(path):
            call_count[0] += 1
            if call_count[0] == 1:
                return False
            return True

        monkeypatch.setattr("src.utils.torrent.validate_path_for_subprocess", mock_validate)

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(ValueError) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "Invalid path" in str(exc_info.value)

    def test_create_torrent_invalid_output_path(self, tmp_path, monkeypatch):
        """Verify torrent creation rejects invalid output path."""
        call_count = [0]

        def mock_validate(path):
            call_count[0] += 1
            if call_count[0] == 2:
                return False
            return True

        monkeypatch.setattr("src.utils.torrent.validate_path_for_subprocess", mock_validate)

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(ValueError) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "Invalid output path" in str(exc_info.value)

    @patch("src.utils.torrent.subprocess.run")
    def test_create_torrent_mktorrent_not_found(self, mock_run, tmp_path):
        """Verify error message mentions install instructions when mktorrent is missing."""
        mock_run.side_effect = FileNotFoundError("No such file or directory: 'mktorrent'")

        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").write_bytes(b"\x00" * 1024)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        with pytest.raises(Exception) as exc_info:
            create_torrent(test_dir, "Test-Release", out_dir)
        assert "mktorrent not installed" in str(exc_info.value)
        assert "brew install mktorrent" in str(exc_info.value) or "apt install mktorrent" in str(exc_info.value)
