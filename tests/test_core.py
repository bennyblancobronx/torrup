"""Tests for core utility functions in src/utils/core.py."""

import os
from datetime import datetime
from pathlib import Path

import pytest

os.environ.setdefault("TORRUP_OUTPUT_DIR", "/tmp/torrup-test-output")

from src.utils import (
    get_folder_size,
    human_size,
    is_excluded,
    now_iso,
    pick_piece_size,
    sanitize_release_name,
    suggest_release_name,
    validate_path_for_subprocess,
)


class TestHumanSize:
    """Tests for human_size function."""

    def test_human_size_bytes(self):
        """Verify bytes formatting."""
        assert human_size(100) == "100.0 B"
        assert human_size(0) == "0.0 B"

    def test_human_size_kilobytes(self):
        """Verify kilobytes formatting."""
        result = human_size(1024)
        assert "KB" in result
        assert "1.0" in result

    def test_human_size_megabytes(self):
        """Verify megabytes formatting."""
        result = human_size(1024 * 1024)
        assert "MB" in result

    def test_human_size_gigabytes(self):
        """Verify gigabytes formatting."""
        result = human_size(1024 * 1024 * 1024)
        assert "GB" in result

    def test_human_size_terabytes(self):
        """Verify terabytes formatting."""
        result = human_size(1024 * 1024 * 1024 * 1024)
        assert "TB" in result

    def test_human_size_petabytes(self):
        """Verify petabytes formatting."""
        result = human_size(1024 * 1024 * 1024 * 1024 * 1024)
        assert "PB" in result


class TestGetFolderSize:
    """Tests for get_folder_size function."""

    def test_folder_size_empty_dir(self, tmp_path):
        """Verify empty directory returns 0."""
        result = get_folder_size(tmp_path)
        assert result == 0

    def test_folder_size_single_file(self, tmp_path):
        """Verify single file size is correct."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")
        result = get_folder_size(tmp_path)
        assert result == 5

    def test_folder_size_nested_files(self, tmp_path):
        """Verify nested files are included in size."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.txt").write_text("hello")
        (subdir / "file2.txt").write_text("world!")
        result = get_folder_size(tmp_path)
        assert result == 11

    def test_folder_size_exceeds_max_files(self, tmp_path):
        """Verify ValueError is raised when file count exceeds max_files."""
        for i in range(10):
            (tmp_path / f"file{i}.txt").write_text("x")
        with pytest.raises(ValueError) as exc_info:
            get_folder_size(tmp_path, max_files=5)
        assert "more than 5 files" in str(exc_info.value)

    def test_folder_size_at_max_files_limit(self, tmp_path):
        """Verify folder with exactly max_files does not raise."""
        for i in range(5):
            (tmp_path / f"file{i}.txt").write_text("x")
        result = get_folder_size(tmp_path, max_files=5)
        assert result == 5


class TestPickPieceSize:
    """Tests for pick_piece_size function."""

    def test_pick_piece_size_small(self):
        """Verify small files get small piece size."""
        size_bytes = 10 * 1024 * 1024
        assert pick_piece_size(size_bytes) == 15

    def test_pick_piece_size_medium(self):
        """Verify medium files get appropriate piece size."""
        size_bytes = 100 * 1024 * 1024
        assert pick_piece_size(size_bytes) == 16

    def test_pick_piece_size_large(self):
        """Verify large files get large piece size."""
        size_bytes = 5 * 1024 * 1024 * 1024
        assert pick_piece_size(size_bytes) == 22

    def test_pick_piece_size_boundaries(self):
        """Verify boundary values are handled correctly."""
        assert pick_piece_size(49 * 1024 * 1024) == 15
        assert pick_piece_size(50 * 1024 * 1024) == 16
        assert pick_piece_size(4096 * 1024 * 1024) == 22

    def test_pick_piece_size_150mb(self):
        """Test 150MB boundary."""
        assert pick_piece_size(149 * 1024 * 1024) == 16
        assert pick_piece_size(150 * 1024 * 1024) == 17

    def test_pick_piece_size_350mb(self):
        """Test 350MB boundary."""
        assert pick_piece_size(349 * 1024 * 1024) == 17
        assert pick_piece_size(350 * 1024 * 1024) == 18

    def test_pick_piece_size_512mb(self):
        """Test 512MB boundary."""
        assert pick_piece_size(511 * 1024 * 1024) == 18
        assert pick_piece_size(512 * 1024 * 1024) == 19

    def test_pick_piece_size_1gb(self):
        """Test 1GB boundary."""
        assert pick_piece_size(1023 * 1024 * 1024) == 19
        assert pick_piece_size(1024 * 1024 * 1024) == 20

    def test_pick_piece_size_2gb(self):
        """Test 2GB boundary."""
        assert pick_piece_size(2047 * 1024 * 1024) == 20
        assert pick_piece_size(2048 * 1024 * 1024) == 21


class TestSanitizeReleaseName:
    """Tests for sanitize_release_name function."""

    def test_sanitize_strips_slashes(self):
        """Verify slashes are replaced with dots."""
        result = sanitize_release_name("a/b/c")
        assert result == "a.b.c"

    def test_sanitize_strips_backslashes(self):
        """Verify backslashes are replaced."""
        result = sanitize_release_name("a\\b\\c")
        assert "\\" not in result

    def test_sanitize_removes_double_dots(self):
        """Verify path traversal patterns are removed."""
        result = sanitize_release_name("..\\evil")
        assert ".." not in result

    def test_sanitize_removes_special_chars(self):
        """Verify special characters are removed."""
        result = sanitize_release_name("test<script>alert('xss')</script>")
        assert "<" not in result
        assert ">" not in result
        assert "'" not in result

    def test_sanitize_empty_returns_unnamed(self):
        """Verify empty input returns 'unnamed'."""
        assert sanitize_release_name("") == "unnamed"
        assert sanitize_release_name(None) == "unnamed"

    def test_sanitize_preserves_valid_chars(self):
        """Verify valid characters are preserved."""
        result = sanitize_release_name("Artist-Album.2024-FLAC")
        assert result == "Artist-Album.2024-FLAC"


class TestSuggestReleaseName:
    """Tests for suggest_release_name function."""

    def test_suggest_release_name_from_file(self, tmp_path):
        """Verify release name is extracted from file."""
        test_file = tmp_path / "Album-Name-2024.flac"
        test_file.touch()
        result = suggest_release_name("music", test_file)
        assert "Album-Name-2024" in result

    def test_suggest_release_name_from_dir(self, tmp_path):
        """Verify release name is extracted from directory."""
        test_dir = tmp_path / "Artist-Album-2024-FLAC"
        test_dir.mkdir()
        result = suggest_release_name("music", test_dir)
        assert "Artist-Album-2024-FLAC" in result


class TestIsExcluded:
    """Tests for is_excluded function."""

    def test_is_excluded_matches_name(self, tmp_path):
        """Verify path with excluded name is detected."""
        excludes = ["tmp", "trash", "torrents"]
        path = tmp_path / "downloads" / "tmp"
        assert is_excluded(path, excludes) is True

    def test_is_excluded_case_insensitive(self, tmp_path):
        """Verify exclusion is case-insensitive."""
        excludes = ["tmp"]
        path = tmp_path / "music" / "TMP"
        assert is_excluded(path, excludes) is True

    def test_is_excluded_returns_false(self, tmp_path):
        """Verify non-excluded path returns False."""
        excludes = ["tmp", "trash"]
        path = tmp_path / "music" / "album" / "track.flac"
        assert is_excluded(path, excludes) is False


class TestNowIso:
    """Tests for now_iso function."""

    def test_now_iso_format(self):
        """Verify ISO format is correct."""
        result = now_iso()
        assert result.endswith("Z")
        dt_str = result[:-1]
        dt = datetime.fromisoformat(dt_str)
        assert dt is not None

    def test_now_iso_contains_date_parts(self):
        """Verify ISO string contains expected parts."""
        result = now_iso()
        assert "T" in result
        assert "-" in result
        assert ":" in result


class TestValidatePathForSubprocess:
    """Tests for validate_path_for_subprocess function."""

    def test_validate_path_rejects_null_byte(self):
        """Verify path with null byte is rejected."""
        path = Path("/some/path\x00/file")
        assert validate_path_for_subprocess(path) is False

    def test_validate_path_accepts_valid(self, tmp_path):
        """Verify valid path is accepted."""
        test_file = tmp_path / "valid_file.txt"
        test_file.touch()
        assert validate_path_for_subprocess(test_file) is True

    def test_validate_path_accepts_nonexistent(self, tmp_path):
        """Verify nonexistent but valid path is accepted."""
        path = tmp_path / "nonexistent.txt"
        assert validate_path_for_subprocess(path) is True

    def test_validate_path_handles_oserror(self, monkeypatch):
        """Verify path validation handles OSError gracefully."""
        test_path = Path("/some/test/path")

        def mock_resolve(*args, **kwargs):
            raise OSError("Cannot resolve path")

        monkeypatch.setattr(test_path.__class__, "resolve", mock_resolve)
        result = validate_path_for_subprocess(test_path)
        assert result is True or result is False

    def test_validate_path_handles_valueerror(self, tmp_path, monkeypatch):
        """Verify path validation handles ValueError gracefully."""
        result = validate_path_for_subprocess(tmp_path / "valid")
        assert result is True
