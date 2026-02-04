"""Utility functions for file operations and torrent creation."""

from src.utils.core import (
    get_folder_size,
    human_size,
    is_excluded,
    now_iso,
    sanitize_release_name,
    suggest_release_name,
    validate_path_for_subprocess,
)
from src.utils.metadata import (
    _extract_album_art,
    _extract_video_thumbnail,
    _find_primary_file,
    _normalize_metadata,
    extract_all_album_art,
    extract_metadata,
    extract_thumbnail,
    write_xml_metadata,
)
from src.utils.nfo import (
    _extract_format,
    _extract_resolution,
    _extract_source,
    _format_metadata_section,
    generate_nfo,
)
from src.utils.torrent import (
    create_torrent,
    pick_piece_size,
)

__all__ = [
    # core
    "get_folder_size",
    "human_size",
    "is_excluded",
    "now_iso",
    "sanitize_release_name",
    "suggest_release_name",
    "validate_path_for_subprocess",
    # metadata
    "_extract_album_art",
    "_extract_video_thumbnail",
    "_find_primary_file",
    "_normalize_metadata",
    "extract_all_album_art",
    "extract_metadata",
    "extract_thumbnail",
    "write_xml_metadata",
    # nfo
    "_extract_format",
    "_extract_resolution",
    "_extract_source",
    "_format_metadata_section",
    "generate_nfo",
    # torrent
    "create_torrent",
    "pick_piece_size",
]
