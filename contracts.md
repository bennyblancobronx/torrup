# Contracts

External integrations, dependencies, and obligations.

## External Services

### Tracker API (currently supports TorrentLeech)

| Endpoint | URL | Purpose |
|----------|-----|---------|
| Upload | `https://www.torrentleech.org/torrents/upload/apiupload` | Upload torrent + NFO |
| Download | `https://www.torrentleech.org/torrents/upload/apidownload` | Download official .torrent after upload |
| Search | `https://www.torrentleech.org/api/torrentsearch` | Duplicate check |
| Tracker | `https://tracker.torrentleech.org` | Announce base URL |

**Authentication:** Single key (e.g. TorrentLeech Passkey) via `TL_ANNOUNCE_KEY` env var.

**Announce URL format (TL):** `https://tracker.torrentleech.org/a/<passkey>/announce`

**Rate Limits:** None documented. Use responsibly.

### qBitTorrent API

| Service | URL | Purpose |
|---------|-----|---------|
| qBitTorrent | Configurable (e.g. `http://localhost:8080`) | Auto-seeding after upload |

**Authentication:** WebUI credentials or environment variable overrides.

**Rate Limits:** Local API, no external limits.

**Required Fields (TL):**
- `announcekey` - 32-char passkey
- `category` - Category number (see docs/torrentleech/torrentleech.md)
- `torrent` - .torrent file (multipart)
- `nfo` - NFO file (multipart)

**Optional Fields (TL):**
- `tags` - Comma-separated tags
- `imdb` - IMDB ID in tt1234567 format (movies/tv)
- `tvmazeid` - TVMaze show ID (TV)
- `tvmazetype` - TVMaze type: 1 for boxsets, 2 for episodes (TV)

**Response:**
- Success: Numeric torrent ID
- Failure: Error text

### ntfy Push Notifications

| Service | URL | Purpose |
|---------|-----|---------|
| ntfy | Configurable (e.g. `https://ntfy.sh`) | Activity warning notifications |

**Authentication:** None (public topics) or server-dependent.

**Usage:** Sends HTTP POST to `<ntfy_url>/<ntfy_topic>` with Title and Priority headers when activity drops below minimum. Controlled by `ntfy_enabled`, `ntfy_url`, `ntfy_topic` settings.

## External Tools

### mediainfo

- **Purpose:** Generate NFO content with media metadata
- **Install:** `brew install mediainfo` (macOS) or `apt install mediainfo` (Linux)
- **Usage:** `mediainfo /path/to/file`
- **Required:** Yes - NFO generation fails without it

### mktorrent

- **Purpose:** Create .torrent files
- **Install:** `brew install mktorrent` (macOS) or `apt install mktorrent` (Linux)
- **Usage:** `mktorrent -p -a URL -s TAG -l SIZE -o OUTPUT PATH`
- **Required:** Yes - torrent creation fails without it

### exiftool

- **Purpose:** Extract embedded metadata from media files (artist, album, title, IDs, lyrics flags, etc.)
- **Install:** `brew install exiftool` (macOS) or `apt install libimage-exiftool-perl` (Linux)
- **Usage:** Called via `extract_metadata()` in src/utils/metadata.py
- **Required:** No - metadata extraction is optional (controlled by `extract_metadata` setting)

### ffmpeg/ffprobe

- **Purpose:** Extract video thumbnails and album artwork; ffprobe augments audio stream details for music NFOs
- **Install:** `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- **Usage:** Called via `extract_thumbnail()` and ffprobe helpers in `src/utils/metadata.py`
- **Required:** No - thumbnail extraction is optional (controlled by `extract_thumbnails` setting)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TL_ANNOUNCE_KEY` | Yes | - | Tracker passkey (e.g. TorrentLeech 32 chars) |
| `SECRET_KEY` | Yes | - | Flask session key (app will not start without this) |
| `TORRUP_DB_PATH` | No | ./torrup.db | SQLite database path |
| `TORRUP_OUTPUT_DIR` | No | ./output | Output directory for torrents/NFOs |
| `TORRUP_RUN_WORKER` | No | 1 | Enable background worker (1=yes, 0=no) |
| `QBT_URL` | No | - | qBitTorrent WebUI URL override |
| `QBT_USER` | No | - | qBitTorrent username override |
| `QBT_PASS` | No | - | qBitTorrent password override |

## Data Storage

### SQLite Database

**Tables:**
- `settings` - Key-value configuration (key TEXT PRIMARY KEY, value TEXT)
  - Notable keys: `output_dir`, `exclude_dirs`, `release_group`, `auto_scan_interval`, `enable_auto_upload`, `extract_metadata`, `extract_thumbnails`, `test_mode`
  - qBT keys: `qbt_enabled`, `qbt_url`, `qbt_user`, `qbt_pass`
  - Activity keys: `tl_min_uploads_per_month`, `tl_min_seed_copies`, `tl_min_seed_days`, `tl_inactivity_warning_weeks`, `tl_absence_notice_weeks`, `tl_enforce_activity`, `tl_last_critical_state`
  - Notification keys: `ntfy_enabled`, `ntfy_url`, `ntfy_topic`
  - Template keys: `template_movies`, `template_tv`, `template_music`, `template_books`
- `media_roots` - Per-media-type paths and defaults
  - Columns: `media_type` (PK), `path`, `enabled`, `default_category`, `auto_scan`, `last_scan`
- `queue` - Upload queue with status tracking
  - Columns: `id` (PK), `media_type`, `path`, `release_name`, `category`, `tags`, `imdb`, `tvmazeid`, `tvmazetype`, `status`, `message`, `created_at`, `updated_at`, `torrent_path`, `nfo_path`, `xml_path`, `thumb_path`, `certainty_score`, `approval_status`

**Location:** Configurable via `TORRUP_DB_PATH`, defaults to `./torrup.db`

## Docker Integration

**Network:** Designed to run in `vpn-stack` with gluetun routing.

**Volumes:**
- Media library roots (read-only)
- Output directory (read-write)
- Database file (read-write)

**Port:** 5001 (configurable)

## Tracker Module

Tracker configuration is modular. `src/trackers/torrentleech.py` contains all TL-specific config (categories, announce URL format, upload fields). Designed for future multi-tracker support.

## Compliance

### Local Path Constraints

- Queue additions only accept paths that exist, are under the enabled media root for the media type, and are not symlinks.

### Tracker Compliance (example: TorrentLeech)

- Torrent v1 only (no v2 or hybrid)
- Private flag must be set
- Source tag: `TorrentLeech.org`
- Announce URL must include passkey: `/a/<passkey>/announce`
- NFO required for every upload
- Paths must be stripped from MediaInfo output
