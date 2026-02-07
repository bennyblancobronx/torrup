# torrup - Torrent Upload Tool

**Version:** 0.1.10

## What It Is

torrup is a local-first web UI + CLI for creating and uploading torrents. It provides queue-based batch uploads, configurable settings, and support for multiple trackers (initially supporting TorrentLeech).

## What It Does

- Music uploads fully working (browse, queue, prepare, upload)
- Movies, TV, books: browsing and queuing works; metadata lookups (IMDB, TVMaze) not yet wired into uploads
- Queue multiple items for batch upload
- Generate NFO files using MediaInfo (with music enhancements via exiftool + ffprobe, plus local lyrics/artwork when available)
- Create torrents with mktorrent (private flag, source tag)
- Check for duplicates via tracker search API (supports TorrentLeech)
- Upload to trackers via API (supports TorrentLeech)
- Track upload status per item
- Metadata extraction via exiftool (optional, used for richer NFOs)
- Thumbnail/artwork extraction via ffmpeg/ffprobe (optional)
- CLI with 13 commands for scripting/automation
- Health check endpoint for monitoring
- Security: CSRF, rate limiting, security headers

## Tech Stack

- **Backend:** Python 3.11 + Flask
- **Database:** SQLite
- **External Tools:** mediainfo, mktorrent, exiftool (optional), ffmpeg/ffprobe (optional)
- **Deployment:** Docker (primary), native (secondary)

## Directory Structure

```
torrup/
  src/           - Source code modules
  templates/     - HTML templates
  static/        - Static assets
  docs/          - Documentation
  scripts/       - Utility scripts
  reference/     - Old plugin code for reference
```

## Status

v0.1.9 - Feature complete:
- Web UI for browsing and uploading (6 pages including changelog)
- CLI with 13 commands
- Queue system with background worker
- Auto-scan worker for automatic library scanning
- qBitTorrent integration (auto-seed)
- TL torrent download for correct info hash seeding
- Directory picker for path selection in settings
- Light/Dark/System theme setting
- Activity tracking and enforcement (upload health monitoring)
- Settings management
- Security hardening (CSRF, rate limiting, headers)
- 316 tests passing
- Docker deployment ready

## Roadmap

- v0.1.x - Bug fixes and refinements
- v0.2.x - Metadata lookups (IMDB, TVMaze, MusicBrainz)
- v0.3.x - Desktop wrapper (pywebview)
