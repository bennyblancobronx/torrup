"""Configuration constants and environment settings."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "torrup"
APP_VERSION = "0.1.12"

# Paths
DB_PATH = Path(os.environ.get("TORRUP_DB_PATH", "./torrup.db"))
DEFAULT_OUTPUT_DIR = Path(os.environ.get("TORRUP_OUTPUT_DIR", "./output"))
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Trackers
from src.trackers import torrentleech as tl

TL_TRACKER = tl.TRACKER_BASE
TL_UPLOAD_URL = tl.UPLOAD_URL
TL_SEARCH_URL = tl.SEARCH_URL
ANNOUNCE_KEY = tl.ANNOUNCE_KEY

# Worker
RUN_WORKER = os.environ.get("TORRUP_RUN_WORKER", "1") == "1"

# Media types
MEDIA_TYPES = ["music", "movies", "tv", "books"]

CATEGORY_OPTIONS = tl.CATEGORIES

DEFAULT_TEMPLATES = {
    "movies": "Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup",
    "tv": "Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup",
    "music": "Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup",
    "books": "Title.Author.Year.Format-ReleaseGroup",
}

DEFAULT_RELEASE_GROUP = "torrup"

DEFAULT_EXCLUDES = ".DS_Store,Thumbs.db,torrents,downloads,tmp,trash,incomplete,processing"

# qBitTorrent Defaults
QBT_DEFAULT_URL = "http://localhost:8080"
QBT_DEFAULT_USER = "admin"
QBT_DEFAULT_PASS = "adminadmin"

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
  Uploaded with torrup
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
  Uploaded with torrup
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
                              BASIC INFO
--------------------------------------------------------------------------------
{basic_info}

--------------------------------------------------------------------------------
                              AUDIO DETAILS
--------------------------------------------------------------------------------
{audio_details}

--------------------------------------------------------------------------------
                              LYRICS
--------------------------------------------------------------------------------
{lyrics_section}

--------------------------------------------------------------------------------
                              ALBUM ART
--------------------------------------------------------------------------------
{album_art_section}

--------------------------------------------------------------------------------
                              TECHNICAL INFO
--------------------------------------------------------------------------------
{mediainfo}
--------------------------------------------------------------------------------
  Uploaded with torrup
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
  Uploaded with torrup
  Generated: {timestamp}
================================================================================
""",

}
