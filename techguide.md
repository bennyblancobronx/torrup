# Technical Guide

How TLT works internally.

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
- `settings` - Global configuration (browse_base, output_dir, exclude_dirs, templates)
- `media_roots` - Per-media-type settings (path, enabled, default_category)
- `queue` - Upload queue (path, release_name, category, status, timestamps)

### API Client (src/api.py)

TorrentLeech integration:
- `check_exists(release_name)` - Search API duplicate check
- `upload_torrent(torrent_path, nfo_path, category, tags)` - Upload API

### Utilities (src/utils.py)

Helper functions:
- `generate_nfo(path, release_name, out_dir)` - MediaInfo NFO generation
- `create_torrent(path, release_name, out_dir)` - mktorrent wrapper
- `write_xml_metadata(...)` - XML sidecar output
- `pick_piece_size(total_bytes)` - Optimal piece size calculation

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
- magazines (maps to Books/EBooks category)

### Category Defaults

| Type | Category ID | Label |
|------|-------------|-------|
| music | 31 | Music :: Audio |
| movies | 14 | Movies :: BlurayRip |
| tv | 26 | TV :: Episodes (SD) |
| books | 45 | Books :: EBooks |
| magazines | 45 | Books :: EBooks |

### Naming Templates

Editable in settings:
- movies: `Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup`
- tv: `Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup`
- music: `Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup`
- books: `Title.Author.Year.Format-ReleaseGroup`
- magazines: `Title.Issue.Year.Format-ReleaseGroup`

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

## CLI Commands (Planned)

```bash
tlt settings get
tlt settings set
tlt browse <media_type> [path]
tlt queue add <media_type> <path> [--category N] [--tags csv]
tlt queue list
tlt queue update <id> [--status status]
tlt queue delete <id>
tlt queue run
tlt prepare <id>
tlt upload <id>
tlt check-dup <release_name>
```

## Running

### Development

```bash
python app.py
# Runs on http://localhost:5001
```

### Docker

```bash
docker build -t tlt .
docker run -p 5001:5001 -e TL_ANNOUNCE_KEY=xxx tlt
```

### With Docker Compose

```yaml
services:
  tlt:
    build: .
    ports:
      - "5001:5001"
    environment:
      - TL_ANNOUNCE_KEY=${TL_ANNOUNCE_KEY}
    volumes:
      - /path/to/media:/volume/media:ro
      - ./output:/app/output
      - ./tlt.db:/app/tlt.db
```
