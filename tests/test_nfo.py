"""Tests for NFO generation in src/utils/nfo.py."""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")

from src.utils import generate_nfo, write_xml_metadata
from src.utils.nfo import (
    _extract_format,
    _extract_resolution,
    _extract_source,
    _format_metadata_section,
)


class TestExtractSource:
    """Tests for _extract_source helper function."""

    def test_extract_source_bluray(self):
        """Verify BluRay source is extracted."""
        result = _extract_source("Movie.Name.2024.1080p.BluRay.x264")
        assert result == "BluRay"

    def test_extract_source_webdl(self):
        """Verify WEB-DL source is extracted."""
        result = _extract_source("Show.S01E01.WEB-DL.1080p")
        assert result == "WEB-DL"

    def test_extract_source_webrip(self):
        """Verify WEBRip source is extracted."""
        result = _extract_source("Movie.2024.WEBRip.720p")
        assert result == "WEBRip"

    def test_extract_source_hdtv(self):
        """Verify HDTV source is extracted."""
        result = _extract_source("Show.S02E05.HDTV.x264")
        assert result == "HDTV"

    def test_extract_source_unknown(self):
        """Verify unknown source returns Unknown."""
        result = _extract_source("Some.Random.Name")
        assert result == "Unknown"


class TestExtractResolution:
    """Tests for _extract_resolution helper function."""

    def test_extract_resolution_1080p(self):
        """Verify 1080p is extracted."""
        result = _extract_resolution("Movie.2024.1080p.BluRay")
        assert result == "1080p"

    def test_extract_resolution_720p(self):
        """Verify 720p is extracted."""
        result = _extract_resolution("Show.S01E01.720p.WEB")
        assert result == "720p"

    def test_extract_resolution_2160p(self):
        """Verify 2160p is extracted."""
        result = _extract_resolution("Movie.2024.2160p.UHD")
        assert result == "2160p"

    def test_extract_resolution_4k(self):
        """Verify 4K is extracted."""
        result = _extract_resolution("Movie.2024.4K.HDR")
        assert result == "4K"

    def test_extract_resolution_unknown(self):
        """Verify unknown resolution returns Unknown."""
        result = _extract_resolution("Album.Name.FLAC")
        assert result == "Unknown"


class TestExtractFormat:
    """Tests for _extract_format helper function."""

    def test_extract_format_flac(self, tmp_path):
        """Verify FLAC format is extracted from name."""
        path = tmp_path / "test"
        path.mkdir()
        result = _extract_format("Artist.Album.2024.FLAC", path)
        assert result == "FLAC"

    def test_extract_format_mp3(self, tmp_path):
        """Verify MP3 format is extracted from name."""
        path = tmp_path / "test"
        path.mkdir()
        result = _extract_format("Artist.Album.MP3.320", path)
        assert result == "MP3"

    def test_extract_format_from_file_extension(self, tmp_path):
        """Verify format extracted from file extension."""
        test_file = tmp_path / "test.epub"
        test_file.touch()
        result = _extract_format("Book.Title", test_file)
        assert result == "EPUB"

    def test_extract_format_from_dir_contents(self, tmp_path):
        """Verify format extracted from directory contents."""
        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()
        result = _extract_format("Artist.Album", test_dir)
        assert result == "FLAC"

    def test_extract_format_unknown(self, tmp_path):
        """Verify unknown format returns Unknown."""
        test_dir = tmp_path / "empty"
        test_dir.mkdir()
        result = _extract_format("Something", test_dir)
        assert result == "Unknown"


class TestWriteXmlMetadata:
    """Tests for write_xml_metadata function."""

    def test_write_xml_creates_file(self, tmp_path):
        """Verify XML file is created."""
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        torrent_path = out_dir / "test.torrent"
        nfo_path = out_dir / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        result = write_xml_metadata(
            release_name="Test-Release",
            media_type="music",
            path=tmp_path,
            size_bytes=1024,
            torrent_path=torrent_path,
            nfo_path=nfo_path,
            tags="rock,indie",
            out_dir=out_dir,
        )

        assert result.exists()
        assert result.suffix == ".xml"

    def test_write_xml_contains_required_fields(self, tmp_path):
        """Verify XML contains required fields."""
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        torrent_path = out_dir / "test.torrent"
        nfo_path = out_dir / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        result = write_xml_metadata(
            release_name="Test-Release",
            media_type="music",
            path=tmp_path,
            size_bytes=1024,
            torrent_path=torrent_path,
            nfo_path=nfo_path,
            tags="rock",
            out_dir=out_dir,
        )

        content = result.read_text()
        assert "Test-Release" in content
        assert "music" in content
        assert "rock" in content

    def test_write_xml_with_metadata(self, tmp_path):
        """Verify XML includes custom metadata."""
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        torrent_path = out_dir / "test.torrent"
        nfo_path = out_dir / "test.nfo"
        torrent_path.touch()
        nfo_path.touch()

        metadata = {"artist": "Test Artist", "album": "Test Album"}

        result = write_xml_metadata(
            release_name="Test-Release",
            media_type="music",
            path=tmp_path,
            size_bytes=1024,
            torrent_path=torrent_path,
            nfo_path=nfo_path,
            tags="",
            out_dir=out_dir,
            metadata=metadata,
        )

        content = result.read_text()
        assert "Test Artist" in content
        assert "Test Album" in content

    def test_write_xml_with_thumbnail(self, tmp_path):
        """Verify XML includes thumbnail path."""
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        torrent_path = out_dir / "test.torrent"
        nfo_path = out_dir / "test.nfo"
        thumb_path = out_dir / "thumb.jpg"
        torrent_path.touch()
        nfo_path.touch()
        thumb_path.touch()

        result = write_xml_metadata(
            release_name="Test-Release",
            media_type="music",
            path=tmp_path,
            size_bytes=1024,
            torrent_path=torrent_path,
            nfo_path=nfo_path,
            tags="",
            out_dir=out_dir,
            thumb_path=thumb_path,
        )

        content = result.read_text()
        assert "thumb.jpg" in content


class TestGenerateNfo:
    """Tests for generate_nfo function."""

    @patch("src.utils.nfo.subprocess.run")
    def test_generate_nfo_creates_file(self, mock_run, tmp_path):
        """Verify NFO file is created."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Format: FLAC\nDuration: 3:45"
        )

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "album"
        test_dir.mkdir()
        (test_dir / "track.flac").touch()

        result = generate_nfo(
            path=test_dir,
            release_name="Artist.Album.2024.FLAC",
            out_dir=out_dir,
            media_type="music",
        )

        assert result.exists()
        assert result.suffix == ".nfo"

    @patch("src.utils.nfo.subprocess.run")
    def test_generate_nfo_contains_release_name(self, mock_run, tmp_path):
        """Verify NFO contains release name."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "test"
        test_dir.mkdir()

        result = generate_nfo(
            path=test_dir,
            release_name="Test-Release-Name",
            out_dir=out_dir,
            media_type="movies",
        )

        content = result.read_text()
        assert "Test-Release-Name" in content

    @patch("src.utils.nfo.subprocess.run")
    def test_generate_nfo_with_metadata(self, mock_run, tmp_path):
        """Verify NFO includes metadata section."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "test"
        test_dir.mkdir()

        metadata = {"title": "Movie Title", "year": "2024"}

        result = generate_nfo(
            path=test_dir,
            release_name="Movie.2024.1080p",
            out_dir=out_dir,
            media_type="movies",
            metadata=metadata,
        )

        content = result.read_text()
        assert "Movie Title" in content
        assert "2024" in content

    @patch("src.utils.nfo.subprocess.run")
    def test_generate_nfo_handles_subprocess_error(self, mock_run, tmp_path):
        """Verify NFO handles mediainfo errors gracefully."""
        mock_run.side_effect = subprocess.SubprocessError("mediainfo not found")

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "test"
        test_dir.mkdir()
        (test_dir / "video.mkv").touch()

        result = generate_nfo(
            path=test_dir,
            release_name="Test-Video",
            out_dir=out_dir,
            media_type="movies",
        )

        assert result.exists()
        content = result.read_text()
        assert "not available" in content.lower() or "MediaInfo" in content


class TestFormatMetadataSection:
    """Tests for _format_metadata_section function."""

    def test_format_metadata_empty(self):
        """Verify empty metadata returns empty string."""
        result = _format_metadata_section({}, "movies")
        assert result == ""

    def test_format_metadata_movies(self):
        """Verify movie metadata is formatted correctly."""
        metadata = {"title": "Test Movie", "year": "2024", "description": "A test movie"}
        result = _format_metadata_section(metadata, "movies")
        assert "Test Movie" in result
        assert "2024" in result
        assert "A test movie" in result

    def test_format_metadata_tv(self):
        """Verify TV metadata includes show info."""
        metadata = {
            "title": "Episode Title",
            "show": "Test Show",
            "season": "1",
            "episode": "5"
        }
        result = _format_metadata_section(metadata, "tv")
        assert "Test Show" in result
        assert "Season" in result or "1" in result
        assert "Episode" in result or "5" in result

    def test_format_metadata_music(self):
        """Verify music metadata is formatted correctly."""
        metadata = {
            "artist": "Test Artist",
            "album": "Test Album",
            "track": "Track Name",
            "year": "2024",
            "genre": "Rock"
        }
        result = _format_metadata_section(metadata, "music")
        assert "Test Artist" in result
        assert "Test Album" in result
        assert "Rock" in result

    def test_format_metadata_music_audio_details(self):
        metadata = {
            "format": "FLAC",
            "bitrate": "24bit",
            "sample_rate": "44.1 kHz",
            "bit_depth": "24",
            "channels": "2.0",
        }
        result = _format_metadata_section(metadata, "music")
        assert "FLAC" in result
        assert "24bit" in result
        assert "44.1 kHz" in result
        assert "24 bit" in result
        assert "2.0" in result

    def test_format_metadata_books(self):
        """Verify books metadata is formatted correctly."""
        metadata = {
            "title": "Book Title",
            "author": "Author Name",
            "publisher": "Publisher Co",
            "year": "2023",
            "isbn": "978-1234567890"
        }
        result = _format_metadata_section(metadata, "books")
        assert "Book Title" in result
        assert "Author Name" in result
        assert "978-1234567890" in result

    def test_format_metadata_truncates_long_description(self):
        """Verify long descriptions are truncated."""
        metadata = {"description": "x" * 200}
        result = _format_metadata_section(metadata, "movies")
        assert len(result) < 250


class TestMediainfoPathStripping:
    """Tests for mediainfo output path stripping in generate_nfo."""

    @patch("src.utils.nfo.subprocess.run")
    def test_mediainfo_strips_file_name(self, mock_run, tmp_path):
        """Verify 'File name' lines are removed from mediainfo output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="General\nFile name                                : movie.mkv\nFormat: MKV\n"
        )

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "movie"
        test_dir.mkdir()
        (test_dir / "movie.mkv").touch()

        result = generate_nfo(
            path=test_dir,
            release_name="Test-Movie",
            out_dir=out_dir,
            media_type="movies",
        )

        content = result.read_text()
        assert "File name" not in content

    @patch("src.utils.nfo.subprocess.run")
    def test_mediainfo_strips_folder_name(self, mock_run, tmp_path):
        """Verify 'Folder name' lines are removed from mediainfo output."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="General\nFolder name                              : /home/user/movies\nFormat: MKV\n"
        )

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "movie"
        test_dir.mkdir()
        (test_dir / "movie.mkv").touch()

        result = generate_nfo(
            path=test_dir,
            release_name="Test-Movie",
            out_dir=out_dir,
            media_type="movies",
        )

        content = result.read_text()
        assert "Folder name" not in content

    @patch("src.utils.nfo.subprocess.run")
    def test_mediainfo_strips_absolute_paths(self, mock_run, tmp_path):
        """Verify lines containing absolute paths (' : /') are removed."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="General\nComplete name                            : /home/user/movies/movie.mkv\nFormat: MKV\n"
        )

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        test_dir = tmp_path / "movie"
        test_dir.mkdir()
        (test_dir / "movie.mkv").touch()

        result = generate_nfo(
            path=test_dir,
            release_name="Test-Movie",
            out_dir=out_dir,
            media_type="movies",
        )

        content = result.read_text()
        assert "/home/user/movies/movie.mkv" not in content
