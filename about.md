# Torrup - Torrent uploader for TorrentLeech

**Version:** 0.1.0

## What It Is

Torrup is a local-first web UI for creating and uploading torrents to TorrentLeech. It provides queue-based batch uploads, configurable settings, and a TorrentLeech-compliant upload flow.

## What It Does

- Browse media libraries by type (music, movies, tv, books, magazines)
- Queue multiple items for batch upload
- Generate NFO files using MediaInfo
- Create torrents with mktorrent (private flag, source tag)
- Check for duplicates via TorrentLeech search API
- Upload to TorrentLeech via API
- Track upload status per item

## Tech Stack

- **Backend:** Python 3.11 + Flask
- **Database:** SQLite
- **External Tools:** mediainfo, mktorrent
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

v0.1.0 - Core functionality complete:
- Web UI for browsing and uploading
- Queue system with background worker
- Settings management
- Docker deployment ready

## Roadmap

- v0.1.x - Bug fixes and refinements
- v0.2.x - Metadata lookups (IMDB, TVMaze, MusicBrainz)
- v0.3.x - Desktop wrapper (pywebview)
