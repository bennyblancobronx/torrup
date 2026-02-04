# Torrup - Torrent uploader for TorrentLeech

Simple GUI for browsing a clean media library, queueing items, generating torrents + NFOs, and uploading to TorrentLeech.

## Version

0.1.0

## Features

- Browse media roots by type (music, movies, TV, books, magazines)
- Queue + batch uploads with editable release names and tags
- Duplicate check via TorrentLeech search API
- NFO generation using MediaInfo (file paths stripped)
- .torrent creation via mktorrent with private flag + source tag
- Basic XML sidecar for each prepared release
- Fully editable settings UI

## Prerequisites

- Python 3.11+
- mediainfo (CLI)
- mktorrent (CLI)

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| TL_ANNOUNCE_KEY | Yes | TorrentLeech passkey (32 chars) |
| SECRET_KEY | Yes | Flask session secret (generate below) |
| TORRUP_DB_PATH | No | SQLite DB path (default: ./torrup.db) |
| TORRUP_OUTPUT_DIR | No | Output directory (default: ./output) |
| TORRUP_RUN_WORKER | No | Run background queue worker (default: 1) |
| TORRUP_AUTH_USER | No | Basic auth username (optional) |
| TORRUP_AUTH_PASS | No | Basic auth password (optional) |

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

With optional basic auth:
```bash
docker run --rm -p 5001:5001 \
  -e TL_ANNOUNCE_KEY=your_passkey \
  -e SECRET_KEY=your_generated_key \
  -e TORRUP_AUTH_USER=admin \
  -e TORRUP_AUTH_PASS=your_password \
  -v /volume/media:/volume/media:ro \
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

- 0.1.x - Docker, macOS
- Planned - Linux, Windows

## Roadmap

- 0.2.x - Metadata lookups (IMDB, TVMaze, MusicBrainz)
- 0.3.x - Desktop wrapper (pywebview)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

[MIT](LICENSE)
