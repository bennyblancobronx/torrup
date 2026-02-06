"""TorrentLeech tracker configuration."""

from __future__ import annotations

import os

NAME = "TorrentLeech"
ID = "torrentleech"

# URLs
TRACKER_BASE = "https://tracker.torrentleech.org"
UPLOAD_URL = "https://www.torrentleech.org/torrents/upload/apiupload"
SEARCH_URL = "https://www.torrentleech.org/api/torrentsearch"

# Settings
ANNOUNCE_KEY = os.environ.get("TL_ANNOUNCE_KEY", "")
SOURCE_TAG = "TorrentLeech.org"

# Category IDs
CATEGORIES = {
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
}

def get_announce_url(passkey: str) -> str:
    """Return personalized announce URL."""
    return f"{TRACKER_BASE}/a/{passkey}/announce" if passkey else TRACKER_BASE
