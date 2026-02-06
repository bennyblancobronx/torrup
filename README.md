# torrup - Torrent Upload Tool

Web UI + CLI for browsing media libraries, queuing items, generating torrents + NFOs, and uploading to trackers (starting with TorrentLeech support).

## Version

0.1.2

## Features

- Browse media roots by type (music, movies, TV, books)
- Queue + batch uploads with editable release names and tags
- Duplicate check via tracker search API (supports TorrentLeech)
- NFO generation using MediaInfo (file paths stripped)
- .torrent creation via mktorrent with private flag + source tag
- Metadata extraction via exiftool (optional)
- Thumbnail extraction via ffmpeg (optional)
- CLI with queue, upload, and qBT commands (browse, queue, prepare, upload, settings, qbt)
- Health check endpoint (/health)
- Configurable logging
- qBitTorrent integration (auto-add after upload, optional auto-source monitor)

## Security

- CSRF protection on all POST endpoints
- Rate limiting (Flask-Limiter)
- Security headers (X-Frame-Options, CSP, etc.)
- Input validation and path traversal prevention
- No debug mode in production

## Tests

- 206 passing tests
- 100% code coverage

## Prerequisites

- Python 3.11+
- mediainfo (CLI)
- mktorrent (CLI)
- exiftool (CLI, optional - for metadata extraction)
- ffmpeg (CLI, optional - for thumbnail extraction)

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| TL_ANNOUNCE_KEY | Yes | Tracker passkey (e.g., TorrentLeech 32 chars) |
| SECRET_KEY | Yes | Flask session secret (generate below) |
| TORRUP_DB_PATH | No | SQLite DB path (default: ./torrup.db) |
| TORRUP_OUTPUT_DIR | No | Output directory (default: ./output) |
| TORRUP_RUN_WORKER | No | Run background queue worker (default: 1) |
| QBT_URL | No | qBitTorrent WebUI URL (overrides setting) |
| QBT_USER | No | qBitTorrent WebUI user (overrides setting) |
| QBT_PASS | No | qBitTorrent WebUI password (overrides setting) |

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## qBitTorrent Integration

qBT is optional but production-ready when configured. You can enable it from the Settings UI or CLI.

**Required settings:**
- `qbt_enabled=1`
- `qbt_url`
- `qbt_user`
- `qbt_pass`

**Common settings:**
- `qbt_auto_add=1` (auto-add after upload)
- `qbt_tag` (default `torrup`)

**Auto-source (optional):**
- `qbt_auto_source=1`
- `qbt_source_categories=music,movies,tv`
- `qbt_category_map=movies=Movies-HD,music=Music` (optional mapping)

**CLI examples:**
```bash
torrup settings set qbt_enabled 1
torrup settings set qbt_url http://localhost:8080
torrup settings set qbt_user admin
torrup settings set qbt_pass adminadmin
torrup settings set qbt_auto_add 1
torrup settings set qbt_auto_source 1
torrup settings set qbt_source_categories music,movies,tv
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export TL_ANNOUNCE_KEY=your_passkey
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
python app.py
```

Open: http://localhost:5001

## Docker

```bash
docker build -t torrup .
docker run --rm -p 5001:5001 \
  -e TL_ANNOUNCE_KEY=your_passkey \
  -e SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") \
  -v /volume/media:/volume/media:ro \
  -v /volume/media/torrents:/output:rw \
  torrup
```

## Directory Structure

```
torrup/
  src/           - Source code modules
  templates/     - HTML templates
  static/        - Static assets
  docs/          - Documentation
  scripts/       - Utility scripts
```

## Platform Support

- 0.1.x - Docker
- Planned - macOS, Linux, Windows

## Roadmap

- 0.2.x - Metadata lookups (IMDB, TVMaze, MusicBrainz)
- 0.3.x - Desktop wrapper (pywebview)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

[MIT](LICENSE)
