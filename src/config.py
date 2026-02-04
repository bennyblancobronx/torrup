"""Configuration constants and environment settings."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "Torrup"
APP_VERSION = "0.1.0"

# Paths
DB_PATH = Path(os.environ.get("TORRUP_DB_PATH", "./torrup.db"))
DEFAULT_OUTPUT_DIR = Path(os.environ.get("TORRUP_OUTPUT_DIR", "./output"))
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# TorrentLeech
TL_TRACKER = "https://tracker.torrentleech.org"
TL_UPLOAD_URL = "https://www.torrentleech.org/torrents/upload/apiupload"
TL_SEARCH_URL = "https://www.torrentleech.org/api/torrentsearch"
ANNOUNCE_KEY = os.environ.get("TL_ANNOUNCE_KEY", "")

# Worker
RUN_WORKER = os.environ.get("TORRUP_RUN_WORKER", "1") == "1"

# Media types
MEDIA_TYPES = ["music", "movies", "tv", "books", "magazines"]

CATEGORY_OPTIONS = {
    "music": [
        {"id": 31, "label": "Music :: Audio"},
        {"id": 16, "label": "Music :: Music Videos"},
    ],
    "movies": [
        {"id": 14, "label": "Movies :: BlurayRip"},
        {"id": 13, "label": "Movies :: Bluray"},
        {"id": 37, "label": "Movies :: WEBRip"},
        {"id": 43, "label": "Movies :: HDRip"},
        {"id": 11, "label": "Movies :: DVDRip/DVDScreener"},
        {"id": 12, "label": "Movies :: DVD-R"},
        {"id": 47, "label": "Movies :: 4K"},
        {"id": 29, "label": "Movies :: Documentaries"},
        {"id": 36, "label": "Movies :: Foreign"},
        {"id": 15, "label": "Movies :: Boxsets"},
        {"id": 8, "label": "Movies :: Cam"},
        {"id": 9, "label": "Movies :: TS/TC"},
    ],
    "tv": [
        {"id": 26, "label": "TV :: Episodes (SD)"},
        {"id": 32, "label": "TV :: Episodes HD"},
        {"id": 27, "label": "TV :: BoxSets"},
        {"id": 44, "label": "TV :: Foreign"},
    ],
    "books": [
        {"id": 45, "label": "Books :: EBooks"},
        {"id": 46, "label": "Books :: Comics"},
    ],
    "magazines": [
        {"id": 45, "label": "Books :: EBooks"},
    ],
}

DEFAULT_TEMPLATES = {
    "movies": "Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup",
    "tv": "Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup",
    "music": "Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup",
    "books": "Title.Author.Year.Format-ReleaseGroup",
    "magazines": "Title.Issue.Year.Format-ReleaseGroup",
}

DEFAULT_RELEASE_GROUP = "Torrup"

DEFAULT_EXCLUDES = "torrents,downloads,tmp,trash,incomplete,processing"

# NFO Templates - clean, informative format for each media type
NFO_TEMPLATES = {
    "movies": """================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : Movies
  Source         : {source}
  Resolution     : {resolution}

--------------------------------------------------------------------------------
                              MEDIA INFO
--------------------------------------------------------------------------------
{mediainfo}
--------------------------------------------------------------------------------
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
""",

    "tv": """================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : TV
  Source         : {source}
  Resolution     : {resolution}

--------------------------------------------------------------------------------
                              MEDIA INFO
--------------------------------------------------------------------------------
{mediainfo}
--------------------------------------------------------------------------------
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
""",

    "music": """================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : Music
  Format         : {format}

--------------------------------------------------------------------------------
                              TRACK INFO
--------------------------------------------------------------------------------
{mediainfo}
--------------------------------------------------------------------------------
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
""",

    "books": """================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : Books
  Format         : {format}

--------------------------------------------------------------------------------
                              FILE INFO
--------------------------------------------------------------------------------
  Files          : {file_count}
  Total Size     : {size}

--------------------------------------------------------------------------------
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
""",

    "magazines": """================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : Magazines
  Format         : {format}

--------------------------------------------------------------------------------
                              FILE INFO
--------------------------------------------------------------------------------
  Files          : {file_count}
  Total Size     : {size}

--------------------------------------------------------------------------------
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
""",
}
