"""Tests for thumbnail extraction in src/utils/metadata.py."""

import json
import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")

from src.utils.metadata import (
    _extract_album_art,
    _extract_video_thumbnail,
)


class TestExtractVideoThumbnail:
    """Tests for _extract_video_thumbnail function."""

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_video_thumbnail_success(self, mock_run, tmp_path):
        """Verify video thumbnail extraction succeeds."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=json.dumps({"format": {"duration": "300"}})),
            MagicMock(returncode=0),
        ]

        video_path = tmp_path / "video.mkv"
        video_path.touch()
        out_path = tmp_path / "thumb.jpg"

        out_path.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        result = _extract_video_thumbnail(video_path, out_path)

        assert result == out_path

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_video_thumbnail_ffprobe_failure(self, mock_run, tmp_path):
        """Verify thumbnail extraction handles ffprobe failure."""
        mock_run.side_effect = [
            MagicMock(returncode=1, stdout=""),
            MagicMock(returncode=0),
        ]

        video_path = tmp_path / "video.mkv"
        video_path.touch()
        out_path = tmp_path / "thumb.jpg"

        out_path.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        result = _extract_video_thumbnail(video_path, out_path)

        assert result == out_path

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_video_thumbnail_timeout(self, mock_run, tmp_path):
        """Verify thumbnail extraction handles timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("ffmpeg", 60)

        video_path = tmp_path / "video.mkv"
        video_path.touch()
        out_path = tmp_path / "thumb.jpg"

        result = _extract_video_thumbnail(video_path, out_path)

        assert result is None

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_video_thumbnail_empty_output(self, mock_run, tmp_path):
        """Verify thumbnail extraction returns None when output is empty."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=json.dumps({"format": {"duration": "300"}})),
            MagicMock(returncode=0),
        ]

        video_path = tmp_path / "video.mkv"
        video_path.touch()
        out_path = tmp_path / "thumb.jpg"

        result = _extract_video_thumbnail(video_path, out_path)

        assert result is None

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_video_thumbnail_bad_json(self, mock_run, tmp_path):
        """Verify thumbnail extraction handles bad JSON from ffprobe."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="not json"),
            MagicMock(returncode=0),
        ]

        video_path = tmp_path / "video.mkv"
        video_path.touch()
        out_path = tmp_path / "thumb.jpg"
        out_path.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        result = _extract_video_thumbnail(video_path, out_path)

        assert result == out_path


class TestExtractAlbumArt:
    """Tests for _extract_album_art function."""

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_album_art_success(self, mock_run, tmp_path):
        """Verify album art extraction succeeds."""
        mock_run.return_value = MagicMock(returncode=0)

        audio_path = tmp_path / "track.flac"
        audio_path.touch()
        out_path = tmp_path / "art.jpg"

        out_path.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

        result = _extract_album_art(audio_path, out_path)

        assert result == out_path

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_album_art_no_artwork(self, mock_run, tmp_path):
        """Verify album art extraction returns None when no artwork."""
        mock_run.return_value = MagicMock(returncode=0)

        audio_path = tmp_path / "track.flac"
        audio_path.touch()
        out_path = tmp_path / "art.jpg"

        result = _extract_album_art(audio_path, out_path)

        assert result is None

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_album_art_timeout(self, mock_run, tmp_path):
        """Verify album art extraction handles timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("ffmpeg", 30)

        audio_path = tmp_path / "track.flac"
        audio_path.touch()
        out_path = tmp_path / "art.jpg"

        result = _extract_album_art(audio_path, out_path)

        assert result is None

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_album_art_subprocess_error(self, mock_run, tmp_path):
        """Verify album art extraction handles subprocess error."""
        mock_run.side_effect = subprocess.SubprocessError("ffmpeg failed")

        audio_path = tmp_path / "track.flac"
        audio_path.touch()
        out_path = tmp_path / "art.jpg"

        result = _extract_album_art(audio_path, out_path)

        assert result is None
