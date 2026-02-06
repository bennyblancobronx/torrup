"""Tests for metadata extraction in src/utils/metadata.py."""

import json
import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")

from src.utils import extract_metadata, extract_thumbnail
from src.utils.metadata import (
    _extract_album_art,
    _extract_video_thumbnail,
    _find_primary_file,
    _normalize_metadata,
)


class TestFindPrimaryFile:
    """Tests for _find_primary_file function."""

    def test_find_primary_file_returns_file_directly(self, tmp_path):
        """Verify file is returned directly."""
        test_file = tmp_path / "video.mkv"
        test_file.touch()
        result = _find_primary_file(test_file, "movies")
        assert result == test_file

    def test_find_primary_file_in_directory(self, tmp_path):
        """Verify file is found in directory."""
        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "cover.jpg").touch()
        (test_dir / "track.flac").touch()

        result = _find_primary_file(test_dir, "music")
        assert result is not None
        assert result.suffix == ".flac"

    def test_find_primary_file_movies(self, tmp_path):
        """Verify movie file is found."""
        test_dir = tmp_path / "movie"
        test_dir.mkdir()
        (test_dir / "readme.txt").touch()
        (test_dir / "movie.mkv").touch()

        result = _find_primary_file(test_dir, "movies")
        assert result is not None
        assert result.suffix == ".mkv"

    def test_find_primary_file_none_when_empty(self, tmp_path):
        """Verify None returned when no matching files."""
        test_dir = tmp_path / "empty"
        test_dir.mkdir()

        result = _find_primary_file(test_dir, "music")
        assert result is None


class TestNormalizeMetadata:
    """Tests for _normalize_metadata function."""

    def test_normalize_metadata_movies(self):
        """Verify movie metadata is normalized."""
        raw = {"Title": "Movie Name", "ContentCreateDate": "2024-01-15", "Description": "A movie"}
        result = _normalize_metadata(raw, "movies")
        assert result.get("title") == "Movie Name"
        assert result.get("year") == "2024"
        assert result.get("description") == "A movie"

    def test_normalize_metadata_music(self):
        """Verify music metadata is normalized."""
        raw = {
            "Artist": "Band Name",
            "Album": "Album Title",
            "Title": "Song Name",
            "Year": 2023,
            "Genre": "Rock"
        }
        result = _normalize_metadata(raw, "music")
        assert result.get("artist") == "Band Name"
        assert result.get("album") == "Album Title"
        assert result.get("track") == "Song Name"
        assert result.get("year") == "2023"

    def test_normalize_metadata_books(self):
        """Verify books metadata is normalized."""
        raw = {
            "Title": "Book Name",
            "Author": "Writer Name",
            "Publisher": "Pub Co"
        }
        result = _normalize_metadata(raw, "books")
        assert result.get("title") == "Book Name"
        assert result.get("author") == "Writer Name"

    def test_normalize_metadata_removes_empty(self):
        """Verify empty values are removed."""
        raw = {"Title": "Name", "Year": "", "Description": None}
        result = _normalize_metadata(raw, "movies")
        assert "year" not in result

    def test_normalize_metadata_tv(self):
        """Verify TV metadata includes show info."""
        raw = {
            "Title": "Episode Name",
            "TVShow": "Show Name",
            "TVSeason": "2",
            "TVEpisode": "5"
        }
        result = _normalize_metadata(raw, "tv")
        assert result.get("title") == "Episode Name"
        assert result.get("show") == "Show Name"
        assert result.get("season") == "2"
        assert result.get("episode") == "5"

    def test_normalize_metadata_books_with_publisher(self):
        """Verify books metadata with publisher is normalized."""
        raw = {
            "Title": "Book Name",
            "Publisher": "Pub Co",
            "CreateDate": "2024-06-15"
        }
        result = _normalize_metadata(raw, "books")
        assert result.get("title") == "Book Name"
        assert result.get("publisher") == "Pub Co"
        assert result.get("year") == "2024"


class TestExtractMetadata:
    """Tests for extract_metadata function."""

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_metadata_success(self, mock_run, tmp_path):
        """Verify metadata extraction succeeds."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps([{
                "Title": "Test Movie",
                "ContentCreateDate": "2024-01-15",
                "Description": "A test movie"
            }])
        )

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result.get("title") == "Test Movie"
        assert result.get("year") == "2024"
        assert result.get("description") == "A test movie"

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_metadata_exiftool_failure(self, mock_run, tmp_path):
        """Verify metadata extraction handles exiftool failure."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_metadata_empty_result(self, mock_run, tmp_path):
        """Verify metadata extraction handles empty result."""
        mock_run.return_value = MagicMock(returncode=0, stdout="[]")

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_metadata_timeout(self, mock_run, tmp_path):
        """Verify metadata extraction handles timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("exiftool", 30)

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}

    @patch("src.utils.metadata.subprocess.run")
    def test_extract_metadata_json_error(self, mock_run, tmp_path):
        """Verify metadata extraction handles JSON parse error."""
        mock_run.return_value = MagicMock(returncode=0, stdout="not valid json")

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}

    def test_extract_metadata_no_target_file(self, tmp_path):
        """Verify metadata extraction returns empty when no target file."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = extract_metadata(empty_dir, "movies")

        assert result == {}

    def test_extract_metadata_invalid_path(self, tmp_path, monkeypatch):
        """Verify metadata extraction handles invalid path."""
        def mock_validate(path):
            return False

        monkeypatch.setattr("src.utils.metadata.validate_path_for_subprocess", mock_validate)

        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}


class TestExtractThumbnail:
    """Tests for extract_thumbnail function."""

    @patch("src.utils.metadata._extract_video_thumbnail")
    def test_extract_thumbnail_video(self, mock_extract, tmp_path):
        """Verify video thumbnail extraction is called for movies."""
        mock_extract.return_value = tmp_path / "thumb.jpg"

        test_file = tmp_path / "movie.mkv"
        test_file.touch()
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = extract_thumbnail(test_file, out_dir, "Test-Movie", "movies")

        mock_extract.assert_called_once()
        assert result == tmp_path / "thumb.jpg"

    @patch("src.utils.metadata._extract_album_art")
    def test_extract_thumbnail_music(self, mock_extract, tmp_path):
        """Verify album art extraction is called for music."""
        mock_extract.return_value = tmp_path / "thumb.jpg"

        test_file = tmp_path / "track.flac"
        test_file.touch()
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = extract_thumbnail(test_file, out_dir, "Test-Album", "music")

        mock_extract.assert_called_once()

    def test_extract_thumbnail_no_target_file(self, tmp_path):
        """Verify thumbnail extraction returns None when no target file."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = extract_thumbnail(empty_dir, out_dir, "Test", "movies")

        assert result is None

    def test_extract_thumbnail_invalid_path(self, tmp_path, monkeypatch):
        """Verify thumbnail extraction handles invalid path."""
        def mock_validate(path):
            return False

        monkeypatch.setattr("src.utils.metadata.validate_path_for_subprocess", mock_validate)

        test_file = tmp_path / "video.mkv"
        test_file.touch()
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = extract_thumbnail(test_file, out_dir, "Test", "movies")

        assert result is None

    def test_extract_thumbnail_books_returns_none(self, tmp_path):
        """Verify thumbnail extraction returns None for books."""
        test_file = tmp_path / "book.epub"
        test_file.touch()
        out_dir = tmp_path / "output"
        out_dir.mkdir()

        result = extract_thumbnail(test_file, out_dir, "Test-Book", "books")

        assert result is None


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


class TestExtractMetadataNoExiftool:
    """Tests for extract_metadata when exiftool is missing."""

    @patch("src.utils.metadata.shutil.which", return_value=None)
    def test_extract_metadata_no_exiftool(self, mock_which, tmp_path):
        """Verify returns empty dict when exiftool is not installed."""
        test_file = tmp_path / "movie.mkv"
        test_file.touch()

        result = extract_metadata(test_file, "movies")

        assert result == {}
        mock_which.assert_called_once_with("exiftool")


class TestFindPrimaryFileAudioPriority:
    """Tests for _find_primary_file audio format priority and hidden file skipping."""

    def test_find_primary_file_prefers_flac_over_mp3(self, tmp_path):
        """Verify FLAC is preferred over MP3 when both exist."""
        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.mp3").touch()
        (test_dir / "track.flac").touch()

        result = _find_primary_file(test_dir, "music")

        assert result is not None
        assert result.suffix == ".flac"

    def test_find_primary_file_skips_hidden_files(self, tmp_path):
        """Verify hidden files (starting with dot) are skipped."""
        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / ".hidden.flac").touch()

        result = _find_primary_file(test_dir, "music")

        assert result is None
