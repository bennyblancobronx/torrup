# TLT Plan (TorrentLeechTool)

## Project Summary

Build a local-first GUI upload tool named **TLT - TorrentLeechTool** with queue + batch uploads, configurable settings, and TorrentLeech-compliant upload flow. This is version **v0.1.0**. Metadata lookups are deferred to **0.2.x**.

## Current Findings (Desktop Feasibility)

- Desktop app is feasible by wrapping the existing web UI in a native webview.
- Minimal-code path: keep Flask + HTML, add a tiny desktop wrapper (pywebview) that opens the local server in a native window.
- Packaging requires per-OS builds and bundling `mediainfo` + `mktorrent` binaries or shipping them as external dependencies.
- Mac builds require codesign/notarization for a smooth install experience; Linux/Windows do not require notarization but still need per-OS packaging.

## Scope (v0.1.0)

- 100% CLI first (all actions available via CLI; GUI is a thin layer on top)
- Local web GUI
- Media-type browsing from clean library roots
- Queue + batch uploads with background processing
- Duplicate check via TorrentLeech search API
- NFO generation via MediaInfo (paths stripped)
- Torrent creation via mktorrent (private flag + source tag)
- XML sidecar output per item
- Fully editable settings in the UI

## Media Types

- music
- movies
- tv
- books
- magazines (mapped to Books → EBooks)

## Naming Schema (editable templates)

- movies: `Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup`
- tv: `Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup`
- music: `Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup`
- books: `Title.Author.Year.Format-ReleaseGroup`
- magazines: `Title.Issue.Year.Format-ReleaseGroup`

## Categories (defaults)

- music: `31` (Music :: Audio)
- movies: `14` (Movies :: BlurayRip)
- tv: `26` (TV :: Episodes SD)
- books: `45` (Books :: EBooks)
- magazines: `45` (Books :: EBooks)

All category defaults are editable in settings.

## Paths + Settings

- **Base library root**: `/volume/media`
- **Exclude folders**: `torrents,downloads,tmp,trash,incomplete,processing`
- **Output dir**: configurable in settings
- **Queue DB**: configurable in settings (default `./tlt.db`)
- **Staging**: use qBittorrent content folder only (no separate staging root)
- **Watch folders**: qBittorrent watch folder per media type (for `.torrent` files)

## Core Upload Flow

1. Browse clean library by media type.
2. Select multiple items and add to queue.
3. Background worker processes queue:
   - Link/copy into qBittorrent content folder (staging in-place)
   - Rename within staging to match naming template
   - Generate NFO (MediaInfo)
   - Create torrent (mktorrent)
   - Write XML sidecar
   - Exact duplicate check via TL search API (requires announce key)
   - Upload to TL API
4. Status updates per item (queued, preparing, uploading, success, failed, duplicate)

## Configuration Surface (Settings UI)

- Media roots table (path, enabled, default category)
- Global browse base path
- Output directory
- Exclude folder list
- Naming templates
- qBittorrent content folder (staging target)
- qBittorrent watch folders per media type (drop .torrent files here)

## CLI Surface (required)

All functionality must be callable from CLI; the GUI only wraps these commands.

Planned commands:

- `tlt settings get`
- `tlt settings set`
- `tlt browse <media_type> [path]`
- `tlt queue add <media_type> <path> [--category N] [--tags csv] [--release-name name]`
- `tlt queue list`
- `tlt queue update <id> [--release-name name] [--category N] [--tags csv] [--status status]`
- `tlt queue delete <id>`
- `tlt queue run` (worker loop)
- `tlt prepare <id>` (NFO + torrent + XML only)
- `tlt upload <id>` (upload only)
- `tlt check-dup <release_name>`

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
- **qBittorrent**: watch folder per media type for `.torrent` files; content staging uses the qBittorrent content folder.
- **Environment**: `TL_ANNOUNCE_KEY`, `SECRET_KEY`, `TLT_DB_PATH`, `TLT_OUTPUT_DIR`, `TLT_RUN_WORKER`.
- **Dependencies**: install `mediainfo` and `mktorrent` in the image.
- **Access control**: CLI is authoritative; GUI is a thin wrapper.
- **Runbook**: build/start commands and expected URL.
- **Torrent compliance**: v1 only, private flag set, source tag `TorrentLeech.org`, announce URL includes passkey.

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
