# Torrup Plan (Historical)

## Project Summary

Build a local-first GUI upload tool named **Torrup** (Torrent Upload Tool) with queue + batch uploads, configurable settings, and support for trackers (initially TorrentLeech). This is version **v0.1.0**. Metadata lookups are deferred to **0.2.x**.

## Current Findings (Desktop Feasibility)

- Desktop app is feasible by wrapping the existing web UI in a native webview.
- Minimal-code path: keep Flask + HTML, add a tiny desktop wrapper (pywebview) that opens the local server in a native window.
- Packaging requires per-OS builds and bundling `mediainfo` + `mktorrent` binaries or shipping them as external dependencies.
- Mac builds require codesign/notarization for a smooth install experience; Linux/Windows do not require notarization but still need per-OS packaging.

## Scope (v0.1.0)

- Local web GUI (primary)
- CLI planned but not implemented in v0.1.x
- Media-type browsing from clean library roots
- Queue + batch uploads with background processing
- Duplicate check via tracker search API (supports TorrentLeech)
- NFO generation via MediaInfo (paths stripped)
- Torrent creation via mktorrent (private flag + source tag)
- XML sidecar output per item
- Fully editable settings in the UI

## Media Types

- music
- movies
- tv
- books

## Naming Schema (editable templates)

- movies: `Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup`
- tv: `Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup`
- music: `Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup`
- books: `Title.Author.Year.Format-ReleaseGroup`

## Categories (defaults)

- music: `31` (Music :: Audio)
- movies: `14` (Movies :: BlurayRip)
- tv: `26` (TV :: Episodes SD)
- books: `45` (Books :: EBooks)

All category defaults are editable in settings.

## Paths + Settings

- **Base library root**: `/volume/media`
- **Exclude folders**: `torrents,downloads,tmp,trash,incomplete,processing`
- **Output dir**: configurable in settings
- **Queue DB**: configurable in settings (default `./torrup.db`)
- **Staging**: use qBittorrent content folder only (no separate staging root)
- **Watch folders**: qBittorrent watch folder per media type (for `.torrent` files)

## Core Upload Flow

1. Browse clean library by media type.
2. Select multiple items and add to queue.
3. Background worker processes queue:
   - Generate NFO (MediaInfo)
   - Create torrent (mktorrent)
   - Write XML sidecar
   - Exact duplicate check via tracker search API (supports TorrentLeech)
   - Upload to tracker API
4. Status updates per item (queued, preparing, uploading, success, failed, duplicate)

## Configuration Surface (Settings UI)

- Media roots table (path, enabled, default category)
- Global browse base path
- Output directory
- Exclude folder list
- Naming templates
- qBittorrent integration is partial (auto-add + monitor exist; watch folders/staging still deferred)

## CLI Surface (planned)

CLI is planned for v0.2.x; GUI is currently primary.

Planned commands:

- `torrup settings get`
- `torrup settings set`
- `torrup browse <media_type> [path]`
- `torrup queue add <media_type> <path> [--category N] [--tags csv] [--release-name name]`
- `torrup queue list`
- `torrup queue update <id> [--release-name name] [--category N] [--tags csv] [--status status]`
- `torrup queue delete <id>`
- `torrup queue run` (worker loop)
- `torrup prepare <id>` (NFO + torrent + XML only)
- `torrup upload <id>` (upload only)
- `torrup check-dup <release_name>`

## Version Roadmap

- **v0.1.0**: Local GUI + queue + uploads + settings
- **v0.2.x**: Metadata lookups (IMDB/TVMaze/MusicBrainz), richer naming auto-fill

## Desktop + Docker Release Plan (order required)

1. **Docker first**
   - Containerized web UI + worker.
   - Volumes: clean library roots (read-only), output dir (read-write).
   - Runs inside existing `vpn-stack` with gluetun + qBittorrent.
   - Config in settings; no external metadata lookups.

2. **macOS second**
   - Add lightweight desktop wrapper that launches the local server and opens a native window.
   - Bundle `mediainfo` + `mktorrent` for macOS or document the install requirement.
   - Codesign/notarize if distribution outside local use is required.

3. **Linux third**
   - Same wrapper approach.
   - Provide AppImage or distro-specific packaging; bundle or depend on `mediainfo` + `mktorrent`.

4. **Windows fourth**
   - Same wrapper approach with Windows webview.
   - Bundle `mediainfo` + `mktorrent` for Windows or document the install requirement.

## Phase 1 Docker Checklist (to completion)

- **Compose wiring**: service name, build context, container name, ports, restart policy, and healthcheck.
- **Network**: attach to `vpn-stack` and route through gluetun.
- **Volumes**: library roots read-only, output dir read-write, DB location persisted.
- **qBittorrent**: partial integration (auto-add/monitor). Watch folder or staging integration is still deferred in v0.1.x.
- **Environment**: `TL_ANNOUNCE_KEY`, `SECRET_KEY`, `TORRUP_DB_PATH`, `TORRUP_OUTPUT_DIR`, `TORRUP_RUN_WORKER`.
- **Dependencies**: install `mediainfo` and `mktorrent` in the image.
- **Access control**: GUI-only in v0.1.x; consider CLI when implemented.
- **Runbook**: build/start commands and expected URL.
- **Torrent compliance**: v1 only, private flag set, source tag (e.g. `TorrentLeech.org`), announce URL includes passkey (e.g. at `/a/<passkey>/announce`).

## Source Docs and References (local copies)

- **TorrentLeech docs**: `projects/tlt/docs/torrentleech/` (PDFs + `torrentleech.md`)
- **Old plugin reference**: `projects/tlt/reference/old-plugin/` (API client + category mapping)

## Open Decisions

- Docker/compose wiring (which compose file + port mapping)
- Any additional media types or rules
## Error Policy (recommended)

- **Duplicate found**: mark item as `duplicate` and stop that item (no upload).
- **Missing tools** (`mediainfo`/`mktorrent`): fail with clear error and do not upload.
- **Upload failure**: mark `failed` with error message; allow manual retry.

## Logging (standard)

- Log to stdout for Docker (structured JSON lines).
- Persist per-item status messages in the queue DB.
- Log levels: `INFO`, `WARN`, `ERROR`.
- Include item id, media type, release name, and step in each log line.
- Log fields: `ts`, `level`, `event`, `item_id`, `media_type`, `release_name`, `step`, `message`, optional `error`.

## Upload History (required)

- Store a persistent upload history table in the same SQLite DB (no new dependencies).
- Fields: `id`, `torrent_id`, `release_name`, `media_type`, `category`, `tags`, `torrent_path`, `nfo_path`, `xml_path`, `created_at`, `status`, `message`.
- Expose via CLI: `tlt uploads list` and `tlt uploads show <id>`.
