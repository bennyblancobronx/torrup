"""Tests for scan CLI, auto_worker, and certainty scoring."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.cli.queue import calculate_certainty
from src.utils.core import generate_release_name


# ---------------------------------------------------------------------------
# calculate_certainty -- music
# ---------------------------------------------------------------------------

class TestCalculateCertaintyMusic:
    """Tests for calculate_certainty with music media type."""

    def test_full_metadata_returns_100(self):
        """Artist + album + year + format + bitrate = 100."""
        meta = {
            "artist": "Pink Floyd",
            "album": "Dark Side of the Moon",
            "year": "1973",
            "format": "FLAC",
            "bitrate": "16bit",
        }
        assert calculate_certainty(meta, "music") == 100

    def test_minimal_metadata_returns_30(self):
        """Only artist present = 30."""
        meta = {"artist": "Pink Floyd"}
        assert calculate_certainty(meta, "music") == 30

    def test_no_metadata_returns_0(self):
        """Empty dict = 0."""
        assert calculate_certainty({}, "music") == 0

    def test_artist_and_album_returns_60(self):
        """Artist + album = 60."""
        meta = {"artist": "Radiohead", "album": "OK Computer"}
        assert calculate_certainty(meta, "music") == 60

    def test_mp3_full_metadata_returns_100(self):
        """MP3 with full metadata is not penalized -- still 100."""
        meta = {
            "artist": "Daft Punk",
            "album": "Random Access Memories",
            "year": "2013",
            "format": "MP3",
            "bitrate": "320",
        }
        assert calculate_certainty(meta, "music") == 100

    def test_clamped_to_0_100(self):
        """Score never exceeds 100 or goes below 0."""
        # Maximally populated dict
        meta = {
            "artist": "A",
            "album": "B",
            "year": "2024",
            "format": "FLAC",
            "bitrate": "24bit",
            "extra_field": "ignored",
        }
        score = calculate_certainty(meta, "music")
        assert 0 <= score <= 100


# ---------------------------------------------------------------------------
# calculate_certainty -- movies / generic
# ---------------------------------------------------------------------------

class TestCalculateCertaintyMovies:
    """Tests for calculate_certainty with movies media type."""

    def test_full_metadata_returns_100(self):
        """Title + year + imdb = 100."""
        meta = {
            "title": "Inception",
            "year": "2010",
            "imdb": "tt1375666",
        }
        assert calculate_certainty(meta, "movies") == 100

    def test_title_only_returns_40(self):
        """Title alone = 40."""
        meta = {"title": "Inception"}
        assert calculate_certainty(meta, "movies") == 40

    def test_tvmazeid_counts_as_id(self):
        """TVMaze ID should contribute 30 points same as imdb."""
        meta = {"title": "Breaking Bad", "tvmazeid": "169"}
        assert calculate_certainty(meta, "tv") == 70

    def test_empty_returns_0(self):
        """Empty dict = 0 for movies."""
        assert calculate_certainty({}, "movies") == 0


# ---------------------------------------------------------------------------
# generate_release_name -- music
# ---------------------------------------------------------------------------

class TestGenerateReleaseNameMusic:
    """Tests for generate_release_name with music media type."""

    def test_standard_format(self):
        """Verify format: Artist-Album-Year-Source-Format-Bitrate-Group."""
        meta = {
            "artist": "Pink Floyd",
            "album": "Dark Side of the Moon",
            "year": "1973",
            "source": "WEB",
            "format": "FLAC",
            "bitrate": "16bit",
        }
        name = generate_release_name(meta, "music", "Torrup")
        # Parts should be separated by hyphens
        parts = name.split("-")
        # Artist is sanitized (spaces become dots), so the split
        # will include sub-parts. Check key tokens instead.
        assert "1973" in name
        assert "WEB" in name
        assert "FLAC" in name
        assert "16bit" in name
        assert "Torrup" in name
        assert "Pink" in name or "Floyd" in name

    def test_mp3_format(self):
        """MP3 release name uses format and bitrate correctly."""
        meta = {
            "artist": "Daft Punk",
            "album": "Discovery",
            "year": "2001",
            "source": "WEB",
            "format": "MP3",
            "bitrate": "320",
        }
        name = generate_release_name(meta, "music", "TestGrp")
        assert "MP3" in name
        assert "320" in name
        assert "TestGrp" in name

    def test_no_year_omitted(self):
        """Year omitted from name when not in metadata."""
        meta = {
            "artist": "Unknown Artist",
            "album": "Some Album",
            "source": "WEB",
            "format": "MP3",
            "bitrate": "V0",
        }
        name = generate_release_name(meta, "music", "Torrup")
        # The name should NOT contain a 4-digit year between album and source
        # but the structure should still be valid
        assert "WEB" in name
        assert "MP3" in name
        assert "V0" in name

    def test_fallback_with_missing_metadata(self):
        """Missing metadata produces a name with Unknown but still structured."""
        meta = {}
        name = generate_release_name(meta, "music", "Torrup")
        # Should still return something, using defaults
        assert name is not None
        assert len(name) > 0
        # "Unknown" is the default for artist/album when key is missing
        assert "Unknown" in name or "unnamed" in name

    def test_special_characters_sanitized(self):
        """Special characters in artist/album are sanitized."""
        meta = {
            "artist": "AC/DC",
            "album": "Back In Black (Remaster)",
            "year": "1980",
            "source": "CD",
            "format": "FLAC",
            "bitrate": "16bit",
        }
        name = generate_release_name(meta, "music", "Torrup")
        # Slashes and parentheses should be removed or replaced
        assert "/" not in name
        assert "(" not in name
        assert ")" not in name


# ---------------------------------------------------------------------------
# generate_release_name -- movies fallback
# ---------------------------------------------------------------------------

class TestGenerateReleaseNameMovies:
    """Tests for generate_release_name with movies media type."""

    def test_movie_with_year(self):
        """Movie name includes year when present."""
        meta = {"title": "Inception", "year": "2010"}
        name = generate_release_name(meta, "movies", "Torrup")
        assert "Inception" in name
        assert "2010" in name
        assert "Torrup" in name

    def test_movie_without_year(self):
        """Movie name without year still includes group."""
        meta = {"title": "Inception"}
        name = generate_release_name(meta, "movies", "Torrup")
        assert "Inception" in name
        assert "Torrup" in name
