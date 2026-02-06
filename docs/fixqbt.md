# qBitTorrent Integration Audit (Torrup)

This report audits qBitTorrent integration across GUI, CLI, workers, and docs. It includes concrete gaps, risks, and an actionable checklist for a new coder.

## Executive Summary

qBitTorrent integration is **partially implemented**. Core API wiring exists (connect, add-torrent, monitor), but the **CLI and GUI are incomplete**, and **documentation is inconsistent** with code. A new coder can fix this by: exposing missing settings, adding CLI subcommands, and aligning docs with real behavior.

## Scope

Files reviewed:
- `src/utils/qbittorrent.py`
- `src/worker.py`
- `src/auto_worker.py`
- `src/routes.py`
- `templates/settings.html`
- `src/db.py`
- `src/cli/settings.py`
- `docs/CLI_REFERENCE.md`
- `docs/plans/tltplan.md`

## Current Behavior (What Works)

- Connects to qBT WebUI via `qbittorrentapi.Client`.
- Adds torrents after successful upload when `qbt_auto_add=1`.
- Tags torrents with `qbt_tag` (default `Torrup`).
- Has a qBT monitor worker to scan completed downloads when `qbt_auto_source=1`.
- GUI lets you set basic qBT connection settings and test connection.
- Environment variable overrides are supported for credentials and URL.

## Setup Settings (Production-Ready Checklist)

These are the **minimum settings** required to use qBT integration reliably in production.

**Required (connection):**
- `qbt_enabled`: `1`
- `qbt_url`: e.g. `http://localhost:8080` (must be reachable from the app)
- `qbt_user`: WebUI username
- `qbt_pass`: WebUI password

**Common (recommended):**
- `qbt_auto_add`: `1` to auto-add torrents after upload
- `qbt_tag`: tag for Torrup-added torrents (default `Torrup`)

**Auto-source (optional, but fully supported in backend):**
- `qbt_auto_source`: `1` to monitor qBT for completed downloads
- `qbt_source_categories`: comma-separated categories to monitor, default `music,movies,tv`
- `qbt_category_map`: optional map to align media types and qBT categories (CSV or JSON)

**Environment variable overrides (higher priority than DB settings):**
- `QBT_URL`
- `QBT_USER`
- `QBT_PASS`

**Test endpoint (for diagnostics):**
- `POST /api/settings/qbt/test` (returns success + qBT version)

**Quick setup example (CLI):**
```bash
torrup settings set qbt_enabled 1
torrup settings set qbt_url http://localhost:8080
torrup settings set qbt_user admin
torrup settings set qbt_pass adminadmin
torrup settings set qbt_auto_add 1
torrup settings set qbt_tag Torrup
torrup settings set qbt_auto_source 1
torrup settings set qbt_source_categories music,movies,tv
torrup settings set qbt_category_map "movies=Movies-HD,music=Music"
```

## Gaps and Inconsistencies

### 1) Error Handling and Configuration Validation
- `get_qbt_client()` returns `None` for missing URL, invalid settings.
- There is no validation for `qbt_url`, nor friendly config diagnostics beyond "failed to connect."
- **Impact**: Harder troubleshooting.

### 2) Category Mapping Ambiguity
- Auto-add uses `media_type` as qBT category in `src/worker.py`.
- Auto-source uses substring match of qBT categories in `src/auto_worker.py`.
- No explicit category mapping configuration.
- **Impact**: Categories may not align with user qBT configuration.

## Actionable Checklist (New Coder)

### Phase 1: GUI + Settings Parity (Done)
- [x] Add GUI controls for `qbt_auto_source` and `qbt_source_categories`.
- [x] Wire new fields in `templates/settings.html` save handler.
- [x] Update `src/routes.py` `update_settings()` to accept those fields.
- [x] Add display defaults and a GUI hint for categories.

### Phase 2: CLI Enhancements (Done)
- [x] Add `torrup qbt test`, `torrup qbt add`, `torrup qbt monitor --once`.
- [x] Add CLI help docs and exit codes.
- [x] Ensure CLI commands use `get_qbt_client()` and report meaningful errors.

### Phase 3: Documentation Alignment (Done)
- [x] Fix `docs/CLI_REFERENCE.md` by removing `qbt_content_dir` and `qbt_watch_dirs`.
- [x] Update `docs/plans/tltplan.md` to reflect current qBT partial integration.
- [x] Add a “qBT Integration” section in `README.md`.

### Phase 4: Validation and Diagnostics (Medium Priority)
- [x] Add lightweight validation in `get_qbt_client()`:
- [x] URL format check
- [x] Friendly log errors for auth failures
- [x] Add logging in `qbt_monitor_worker` for summary count of completed torrents.

### Phase 5: Category Mapping (Optional)
- [x] Add a settings map `qbt_category_map` (JSON or CSV key/value).
- [x] Use mapping in both auto-add and auto-source.

## Suggested Implementation Notes

- Keep settings keys consistent:
  - `qbt_enabled`, `qbt_url`, `qbt_user`, `qbt_pass`, `qbt_auto_add`, `qbt_tag`, `qbt_auto_source`, `qbt_source_categories`
- Default for `qbt_source_categories`: `music,movies,tv` (already in DB).
- Preserve existing behavior for users who only enable auto-add.

## Quick Verification Steps

1. Enable qBT in GUI and test connection.
2. Enable auto-add, upload an item, confirm torrent appears in qBT.
3. Enable auto-source, set categories, add a completed torrent in qBT, confirm it is queued.
4. Run CLI `torrup settings get qbt_*` to confirm persistence.

## Residual Risks (If Not Fixed)

- Users cannot enable auto-source or categories via GUI.
- Docs mislead contributors about available features.
- qBT category mismatches lead to missing uploads.
