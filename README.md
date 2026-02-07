# torrup - Torrent Upload Tool

Web UI + CLI for browsing media libraries, queuing items, generating torrents + NFOs, and uploading to trackers (starting with TorrentLeech support).

## Version

0.1.10

## Features

- Music uploads fully working (browse, queue, prepare, upload)
- Movies, TV, books: browsing and queuing works; metadata lookups (IMDB, TVMaze) not yet wired into uploads
- Queue + batch uploads with editable release names and tags
- Duplicate check via tracker search API (supports TorrentLeech)
- NFO generation using MediaInfo (file paths stripped) with richer music sections (exiftool + ffprobe + local lyrics/artwork when available)
- .torrent creation via mktorrent with private flag + source tag
- Metadata extraction via exiftool (optional)
- Thumbnail extraction via ffmpeg (optional)
- Auto-scan worker for automatic library scanning
- Manual scan button on dashboard
- Activity tracking and enforcement (upload health monitoring)
- Auto-exclude OS junk files (.DS_Store, Thumbs.db) from browsing and scanning
- Self-cleaning output dir (staging files removed after successful upload)
- CLI with queue, upload, and qBT commands (browse, scan, queue, prepare, upload, settings, activity, qbt)
- Health check endpoint (/health)
- Configurable logging
- qBitTorrent integration (auto-seed after upload)

## Security

- CSRF protection on all POST endpoints
- Rate limiting (Flask-Limiter)
- Security headers (X-Frame-Options, CSP, etc.)
- Input validation and path traversal prevention
- No debug mode in production

## Tests

- 317 passing tests

## Prerequisites

- Python 3.11+
- mediainfo (CLI)
- mktorrent (CLI)
- exiftool (CLI, optional - for richer metadata + music NFO details)
- ffmpeg/ffprobe (CLI, optional - for thumbnail/artwork extraction + audio stream details)

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

qBT is optional. When enabled, torrup downloads TL's official .torrent after upload and sends it to qBT for seeding automatically.

**Settings:**
- `qbt_enabled` - Enable auto-seeding (0/1)
- `qbt_url` - WebUI URL (default: http://localhost:8080)
- `qbt_user` - WebUI username
- `qbt_pass` - WebUI password

Configure via Settings UI or CLI:
```bash
torrup settings set qbt_enabled 1
torrup settings set qbt_url http://localhost:8080
torrup settings set qbt_user admin
torrup settings set qbt_pass yourpassword
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

### Using Docker Compose (Recommended)

```bash
# Create .env with your keys
echo "TL_ANNOUNCE_KEY=your_passkey" >> .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
echo "MEDIA_PATH=/your/media/library" >> .env

# Start
docker compose up -d

# Update to latest
docker compose pull && docker compose up -d
```

The compose file pulls from `ghcr.io/bennyblancobronx/torrup:latest`. Output dir uses tmpfs (self-cleaning cache). Only the database and media library are persistent volumes.

### Building Locally

To build from source instead of pulling the image, edit docker-compose.yml:
```yaml
services:
  torrup:
    # image: ghcr.io/bennyblancobronx/torrup:latest
    build: .
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
