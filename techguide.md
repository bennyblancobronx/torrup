# Technical Guide

How torrup works internally.

## Architecture

```
Browser <-> Flask App <-> SQLite DB
                |
                v
         Background Worker + Auto-Scan Worker
                |
                v
    mediainfo + mktorrent + TL API + qBitTorrent API
```

## Core Components

### Activity Tracking (src/utils/activity.py + src/routes_activity.py + src/cli/activity.py)

Monitors monthly upload activity against a configurable minimum:
- `calculate_health(conn)` - Returns current month stats: uploads, queued, projected, needed, critical flag, pace
- `get_monthly_history(conn, months)` - Upload counts grouped by YYYY-MM for the last N months
- `estimate_pace(conn)` - Uploads per day averaged over the last 7 days
- `send_ntfy(url, topic, title, message)` - Push notification via ntfy service
- `check_and_notify_critical(conn, critical)` - Sends ntfy alert on False->True transition of critical state

Settings that control activity enforcement:
- `tl_min_uploads_per_month` (default 10) - Monthly upload minimum
- `tl_enforce_activity` (default 1) - Enable enforcement (critical flag triggers warnings)
- `ntfy_enabled`, `ntfy_url`, `ntfy_topic` - Push notification config

### Tracker Module (src/trackers/torrentleech.py)

Tracker-specific configuration extracted from config.py:
- Base URLs (site, API, announce)
- Category mappings (ID to label, per media type)
- Source tag and announce key handling
- Imported by config.py so the rest of the app stays tracker-agnostic

### Database (src/db.py)

SQLite with three tables:
- `settings` - Key-value configuration (output_dir, exclude_dirs, release_group, templates, qbt_*, tl_*, ntfy_*)
- `media_roots` - Per-media-type settings (path, enabled, default_category, auto_scan, last_scan)
- `queue` - Upload queue (media_type, path, release_name, category, tags, status, message, timestamps, imdb, tvmazeid, tvmazetype, torrent_path, nfo_path, xml_path, thumb_path, certainty_score, approval_status)

### API Client (src/api.py)

Tracker integration (currently supports TorrentLeech):
- `check_exists(release_name, exact=False)` - Search API duplicate check. Pass `exact=True` for strict matching.
- `upload_torrent(torrent_path, nfo_path, category, tags, imdb=None, tvmazeid=None, tvmazetype=None)` - Upload API with optional external IDs
- `download_torrent(torrent_id, dest_path)` - Download official .torrent from TL after upload (ensures correct info hash for seeding)

### Utilities (src/utils/)

Helper functions (src/utils/core.py, src/utils/nfo.py, src/utils/torrent.py):
- `generate_release_name(metadata, media_type, release_group)` - Build a release name from extracted metadata
- `generate_nfo(path, release_name, out_dir, media_type, release_group, metadata)` - NFO generation using templates
- `create_torrent(path, release_name, out_dir)` - mktorrent wrapper
  - Uses announce URL format `https://tracker.torrentleech.org/a/<passkey>/announce`
- `write_xml_metadata(...)` - XML sidecar output with metadata
- `pick_piece_size(total_bytes)` - Optimal piece size calculation
- `_extract_source(name)` - Extract source type from release name (BluRay, WEB-DL, etc.)
- `_extract_resolution(name)` - Extract resolution from release name (1080p, 4K, etc.)
- `_extract_format(name, path)` - Extract format from release name or file extension

Metadata extraction (exiftool):
- `extract_metadata(path, media_type)` - Extract embedded metadata from files
- `_find_primary_file(path, media_type)` - Find best file to extract from
- `_normalize_metadata(raw, media_type)` - Standardize exiftool output

Thumbnail extraction (ffmpeg):
- `extract_thumbnail(path, out_dir, release_name, media_type)` - Extract video frame or album art
- `_extract_video_thumbnail(video_path, out_path)` - Extract frame at 10% duration
- `_extract_album_art(audio_path, out_path)` - Extract embedded album artwork

### Routes (src/routes.py + src/routes_queue.py + src/routes_activity.py)

Page routes (src/routes.py):
- `GET /` - Main UI
- `GET /settings` - Settings UI
- `GET /browse` - Browse media library page
- `GET /queue` - Upload queue page
- `GET /history` - Upload history page

Browse/settings API (src/routes.py):
- `GET /health` - Health check (returns status + version)
- `GET /api/stats` - Dashboard statistics (queue counts, auto-scan status, last scan time)
- `POST /api/settings` - Update settings
- `GET /api/browse` - Browse media folders
- `GET /api/browse-dirs` - Browse filesystem directories (for settings path picker)
- `POST /api/settings/qbt/test` - Test qBitTorrent connection

Queue API routes (src/routes_queue.py):
- `POST /api/queue/add` - Add items to queue
- `GET /api/queue` - List queue
- `POST /api/queue/update` - Update queue item
- `POST /api/queue/delete` - Delete queue item

Activity API routes (src/routes_activity.py):
- `GET /api/activity/health` - Current month activity health status
- `GET /api/activity/history?months=N` - Monthly upload history (default 6 months, max 24)

### Worker (src/worker.py)

Background processing loop:
1. Poll queue for items with status `queued` and `approval_status = 'approved'`
2. Check for duplicates via tracker search API
3. Generate NFO with mediainfo
4. Create torrent with mktorrent
5. Write XML sidecar
6. Upload to tracker
7. Update status (success/failed/duplicate)
8. After each processed item, check activity health and send ntfy notification if critical

### Auto-Scan Worker (src/auto_worker.py)

Background thread that automatically discovers missing uploads:
1. Periodically scans enabled media roots (interval set by `auto_scan_interval`)
2. Skips directories matching `exclude_dirs` setting
3. For music: walks two levels deep (artist/album). For other types: scans immediate children.
4. Checks if content already exists on the tracker (items found are recorded as `duplicate` to avoid re-scanning)
5. Queues missing items automatically with certainty scoring and approval gating
6. Controlled by `enable_auto_upload` (default off) and `auto_scan_interval` settings

### qBitTorrent Utility (src/utils/qbittorrent.py)

Helper for qBitTorrent API communication:
- `get_qbt_client()` - Authenticated client with environment variable overrides (`QBT_URL`, `QBT_USER`, `QBT_PASS`)
- `add_to_qbt(torrent_path, save_path, category)` - Add torrent to qBT for seeding (tag hardcoded as "torrup")

### Queue Path Validation

`/api/queue/add` accepts only paths that:
- Exist on disk
- Are under the enabled media root for the given media type
- Are not symlinks

## Upload Flow

```
1. User browses media library
2. User selects items and adds to queue
3. Worker picks up queued item
4. Duplicate check via tracker API
   - If found: mark as "duplicate", skip
5. Generate NFO (mediainfo)
6. Create .torrent (mktorrent) -- temp file for upload only
7. Write XML metadata
8. Upload to tracker API
   - Success: mark as "success" with torrent ID
   - Failure: mark as "failed" with error
9. If qBT enabled: download TL's official .torrent (correct hash), send to qBT, delete temp
10. Fallback: if TL download fails, seed with local .torrent copy
```

## Configuration

### Media Types

- music
- movies
- tv
- books

### Auto-Scan Settings

| Setting | Default | Description |
|---------|---------|-------------|
| enable_auto_upload | 0 | Enable automatic scanning and queuing (safety first -- off by default) |
| auto_scan_interval | 60 | Minutes between auto-scan cycles |

### qBitTorrent Settings

| Setting | Default | Description |
|---------|---------|-------------|
| qbt_enabled | 0 | Enable qBitTorrent auto-seeding (downloads TL's .torrent and sends to qBT after upload) |
| qbt_url | http://localhost:8080 | qBitTorrent WebUI URL |
| qbt_user | admin | qBitTorrent username |
| qbt_pass | adminadmin | qBitTorrent password |

### Activity Enforcement Settings

| Setting | Default | Description |
|---------|---------|-------------|
| tl_min_uploads_per_month | 10 | Minimum monthly uploads to stay active |
| tl_enforce_activity | 1 | Enable activity enforcement warnings |
| tl_min_seed_copies | 10 | Minimum seed copies threshold |
| tl_min_seed_days | 7 | Minimum days to seed |
| tl_inactivity_warning_weeks | 3 | Weeks before inactivity warning |
| tl_absence_notice_weeks | 4 | Weeks before absence notice |
| ntfy_enabled | 0 | Enable ntfy push notifications |
| ntfy_url | (empty) | ntfy server URL |
| ntfy_topic | (empty) | ntfy topic name |

### Category Defaults

| Type | Category ID | Label |
|------|-------------|-------|
| music | 31 | Music :: Audio |
| movies | 14 | Movies :: BlurayRip |
| tv | 26 | TV :: Episodes (SD) |
| books | 45 | Books :: EBooks |

### Naming Templates

Editable in settings:
- movies: `Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup`
- tv: `Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup`
- music: `Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup`
- books: `Title.Author.Year.Format-ReleaseGroup`

### NFO Templates

Each media type has a structured NFO template (defined in `src/config.py`):

```
================================================================================
                              {release_name}
================================================================================

  Release Group  : {release_group}
  Category       : {category}
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
```

Template variables:
- `{release_name}` - Sanitized release name
- `{release_group}` - From settings (default: torrup)
- `{source}` - Extracted from release name (BluRay, WEB-DL, etc.)
- `{resolution}` - Extracted from release name (1080p, 4K, etc.)
- `{format}` - For music/books (FLAC, EPUB, etc.)
- `{mediainfo}` - Output from mediainfo command
- `{file_count}` - For books
- `{size}` - Human-readable size
- `{timestamp}` - Generation timestamp

## Piece Size Calculation

Based on total content size:

| Size | Piece Size | mktorrent -l |
|------|------------|--------------|
| < 50 MB | 32 KB | 15 |
| 50-150 MB | 64 KB | 16 |
| 150-350 MB | 128 KB | 17 |
| 350-512 MB | 256 KB | 18 |
| 512 MB - 1 GB | 512 KB | 19 |
| 1-2 GB | 1 MB | 20 |
| 2-4 GB | 2 MB | 21 |
| > 4 GB | 4 MB | 22 |

## CLI Architecture

**CLI-first design**: All functionality is accessible via CLI. The GUI is a thin wrapper that calls CLI commands internally.

```
User Input
    |
    v
torrup <command> [subcommand] [args] [--flags]
    |
    v
Command Router (src/cli/__init__.py)
    |
    +---> Settings Module (src/cli/settings.py)
    +---> Browse Module (src/cli/browse.py)
    +---> Queue Module (src/cli/queue.py)
    +---> Upload Module (src/cli/upload.py)
    +---> Scan Module (src/cli/scan.py)
    +---> Activity Module (src/cli/activity.py)
    +---> qBT Module (src/cli/qbt.py)
    |
    v
Output (stdout/stderr + exit codes)
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Resource not found |
| 4 | Duplicate detected |
| 5 | API/network error |
| 6 | Missing dependency (mediainfo/mktorrent) |

### Output Formats

- Default: Human-readable text
- `--json`: JSON output for scripting
- `--quiet`: Suppress non-essential output

## CLI Commands

Full reference: [docs/CLI_REFERENCE.md](docs/CLI_REFERENCE.md)

### Settings

```bash
# Get all settings
torrup settings get

# Get specific setting
torrup settings get <key>

# Set a setting
torrup settings set <key> <value>
```

### Browse

```bash
# Browse media library
torrup browse <media_type> [path]

# Examples
torrup browse music
torrup browse movies /volume/media/movies/2024
```

### Queue Management

```bash
# Add to queue
torrup queue add <media_type> <path> [--category N] [--tags csv] [--release-name name]

# List queue
torrup queue list [--status STATUS] [--media-type TYPE] [--limit N] [--offset N]

# Update queue item
torrup queue update <id> [--release-name name] [--category N] [--tags csv] [--status status] [--approval approved|pending_approval|rejected]

# Delete from queue
torrup queue delete <id>

# Run worker (process queue)
torrup queue run [--once] [--interval N]
```

### Scan

```bash
# Scan a library for content missing from the tracker
torrup scan <media_type> <path>

# Options
torrup scan music /volume/media/music --recursive
torrup scan music /volume/media/music --dry-run
```

Currently supports music scanning (walks artist/album directories).

### Prepare and Upload

```bash
# Prepare only (NFO + torrent + XML)
torrup prepare <id>

# Upload only (assumes prepared)
torrup upload <id>

# Check for duplicates
torrup check-dup <release_name>
```

### Upload History

```bash
# List upload history
torrup uploads list [--limit N] [--status STATUS] [--media-type TYPE] [--since YYYY-MM-DD]

# Show upload details
torrup uploads show <id>
```

### Activity

```bash
# Show TL activity health for the current month
torrup activity
torrup activity --json
```

Displays: uploads this month, queued count, projected vs minimum, needed uploads, days remaining, enforcement status, and 7-day upload pace.

### qBitTorrent

```bash
# Test qBitTorrent connection
torrup qbt test

# Add a torrent to qBitTorrent
torrup qbt add --torrent /path/to/file.torrent --save-path /path/to/content [--category CAT]
```

## Running

### Development

```bash
python app.py
# Runs on http://localhost:5001
```

### Docker

```bash
docker build -t torrup .
docker run -p 5001:5001 -e TL_ANNOUNCE_KEY=xxx torrup
```

### With Docker Compose

```yaml
services:
  torrup:
    build: .
    ports:
      - "5001:5001"
    environment:
      - TL_ANNOUNCE_KEY=${TL_ANNOUNCE_KEY}
    volumes:
      - /path/to/media:/volume/media:ro
      - ./output:/app/output
      - ./torrup.db:/app/torrup.db
```
