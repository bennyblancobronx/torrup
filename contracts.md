# Contracts

External integrations, dependencies, and obligations.

## External Services

### TorrentLeech API

| Endpoint | URL | Purpose |
|----------|-----|---------|
| Upload | `https://www.torrentleech.org/torrents/upload/apiupload` | Upload torrent + NFO |
| Search | `https://www.torrentleech.org/api/torrentsearch` | Duplicate check |
| Tracker | `https://tracker.torrentleech.org` | Announce base URL |

**Authentication:** Single key (Torrent Passkey) via `TL_ANNOUNCE_KEY` env var.

**Announce URL format:** `https://tracker.torrentleech.org/a/<passkey>/announce`

**Rate Limits:** None documented. Use responsibly.

**Required Fields:**
- `announcekey` - 32-char passkey
- `category` - Category number (see docs/torrentleech/torrentleech.md)
- `torrent` - .torrent file
- `nfo` - NFO file or description text

**Response:**
- Success: Numeric torrent ID
- Failure: Error text

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

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TL_ANNOUNCE_KEY` | Yes | - | TorrentLeech passkey |
| `SECRET_KEY` | Yes | - | Flask session key (app will not start without this) |
| `TORRUP_DB_PATH` | No | ./torrup.db | SQLite database path |
| `TORRUP_OUTPUT_DIR` | No | ./output | Output directory for torrents/NFOs |
| `TORRUP_RUN_WORKER` | No | 1 | Enable background worker (1=yes, 0=no) |

## Data Storage

### SQLite Database

**Tables:**
- `settings` - Key-value configuration
- `media_roots` - Per-media-type paths and defaults
- `queue` - Upload queue with status tracking

**Location:** Configurable via `TORRUP_DB_PATH`, defaults to `./torrup.db`

## Docker Integration

**Network:** Designed to run in `vpn-stack` with gluetun routing.

**Volumes:**
- Media library roots (read-only)
- Output directory (read-write)
- Database file (read-write)

**Port:** 5001 (configurable)

## Compliance

### TorrentLeech Requirements

- Torrent v1 only (no v2 or hybrid)
- Private flag must be set
- Source tag: `TorrentLeech.org`
- Announce URL must include passkey: `/a/<passkey>/announce`
- NFO required for every upload
- Paths must be stripped from MediaInfo output
