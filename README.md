# TLT - TorrentLeechTool

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

## Environment

| Variable | Description |
|---------|-------------|
| TL_ANNOUNCE_KEY | TorrentLeech passkey (32 chars) |
| SECRET_KEY | Flask session secret |
| TLT_DB_PATH | SQLite DB path (default: ./tlt.db) |
| TLT_OUTPUT_DIR | Output directory (default: ./output) |
| TLT_RUN_WORKER | Run background queue worker (default: 1) |

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export TL_ANNOUNCE_KEY=your_passkey
python app.py
```

Open: http://localhost:5001

## Docker

```bash
docker build -t tlt .
docker run --rm -p 5001:5001 \
  -e TL_ANNOUNCE_KEY=your_passkey \
  -v /volume/media:/volume/media:ro \
  -v /volume/media/torrents:/output:rw \
  tlt
```

## Notes

- TL naming rules are documented in the linked PDFs from your archive. TLT uses those as guidance and lets you edit per item.
- Metadata lookups (IMDB/TVMaze/MusicBrainz) are planned for 0.2.x.
