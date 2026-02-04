# Technical Guide

How Torrup works internally.

## Architecture

```
Browser <-> Flask App <-> SQLite DB
                |
                v
         Background Worker
                |
                v
    mediainfo + mktorrent + TL API
```

## Core Components

### Database (src/db.py)

SQLite with three tables:
- `settings` - Global configuration (browse_base, output_dir, exclude_dirs, release_group, templates)
- `media_roots` - Per-media-type settings (path, enabled, default_category)
- `queue` - Upload queue (path, release_name, category, status, timestamps)

### API Client (src/api.py)

TorrentLeech integration:
- `check_exists(release_name)` - Search API duplicate check
- `upload_torrent(torrent_path, nfo_path, category, tags)` - Upload API

### Utilities (src/utils.py)

Helper functions:
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
- `extract_all_album_art(path, out_dir, release_name)` - Batch extraction for music folders

### Routes (src/routes.py)

Flask endpoints:
- `GET /` - Main UI
- `GET /settings` - Settings UI
- `POST /api/settings` - Update settings
- `GET /api/browse` - Browse media folders
- `POST /api/queue/add` - Add items to queue
- `GET /api/queue` - List queue
- `POST /api/queue/update` - Update queue item
- `POST /api/queue/delete` - Delete queue item

### Worker (src/worker.py)

Background processing loop:
1. Poll queue for items with status `queued`
2. Check for duplicates via TL search API
3. Generate NFO with mediainfo
4. Create torrent with mktorrent
5. Write XML sidecar
6. Upload to TorrentLeech
7. Update status (success/failed/duplicate)

## Upload Flow

```
1. User browses media library
2. User selects items and adds to queue
3. Worker picks up queued item
4. Duplicate check via TL API
   - If found: mark as "duplicate", skip
5. Generate NFO (mediainfo)
6. Create .torrent (mktorrent)
7. Write XML metadata
8. Upload to TL API
   - Success: mark as "success" with torrent ID
   - Failure: mark as "failed" with error
```

## Configuration

### Media Types

- music
- movies
- tv
- books

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
  Uploaded with Torrup
  Generated: {timestamp}
================================================================================
```

Template variables:
- `{release_name}` - Sanitized release name
- `{release_group}` - From settings (default: Torrup)
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
Command Router (src/cli.py)
    |
    +---> Settings Module (src/db.py)
    +---> Browse Module (src/utils.py)
    +---> Queue Module (src/db.py + src/worker.py)
    +---> Upload Module (src/api.py)
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
torrup queue list [--status STATUS] [--limit N]

# Update queue item
torrup queue update <id> [--release-name name] [--category N] [--tags csv] [--status status]

# Delete from queue
torrup queue delete <id>

# Run worker (process queue)
torrup queue run [--once] [--interval N]
```

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
torrup uploads list [--limit N] [--status STATUS]

# Show upload details
torrup uploads show <id>
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
