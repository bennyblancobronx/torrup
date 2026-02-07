# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9] - 2026-02-06

### Added
- Changelog page: GET /changelog renders CHANGELOG.md as styled HTML with version cards
- Version number in header is now a clickable link to /changelog on all pages
- TL torrent download API: after upload, downloads TL's official .torrent (correct info hash) for seeding
- Auto-seed flow: upload to TL -> download TL .torrent -> send to qBT -> delete temp local .torrent
- Fallback: if TL download fails, seeds with local .torrent copy and logs warning

### Changed
- Simplified qBT settings from 10 to 4: qbt_enabled, qbt_url, qbt_user, qbt_pass
- Removed qbt_auto_add (now automatic when qbt_enabled is on)
- Removed qbt_tag (hardcoded as "torrup")
- Removed qbt_auto_source, qbt_source_categories, qbt_category_map (qBT monitor feature removed)
- Removed qBT monitor worker thread (was polling qBT for completed downloads to upload)
- Removed CLI command: torrup qbt monitor
- Removed category mapping functions (parse_qbt_category_map, map_media_type_to_qbt_category, map_qbt_category_to_media_type)
- Settings UI: qBT section now just enabled toggle + URL/user/pass + test button

### Fixed
- is_excluded() false positive on Linux: was checking all path parts including system /tmp, now checks entry name only

### Docs
- Updated techguide.md, contracts.md, CLI_REFERENCE.md, GUI docs to reflect simplified qBT integration

## [0.1.8] - 2026-02-06

### Added
- TL activity enforcement: dashboard + queue warning banners when projected uploads < monthly minimum
- Monthly upload history chart on dashboard (6-month bar chart)
- History page monthly counter
- CLI command: torrup activity (--json supported)
- ntfy push notifications on critical activity transitions (configurable URL + topic)
- API: GET /api/activity/health, GET /api/activity/history
- Auto-worker pace estimation in banner

### Changed
- TL numeric settings now enforce min=0 max=100
- Removed redundant browse_base setting (each media root already has its own path)
- Grayed out movies, tv, books in UI (music only supported for now)
- Header: removed worker status indicator, replaced Settings text with gear icon (right-justified), version number inline after app name, nav hover uses accent color
- Settings page includes ntfy notification configuration

### Docs
- Updated techguide.md: added activity tracking, activity/qbt CLI commands, activity enforcement settings, updated routes listing, updated worker/auto-scan/qbt-monitor descriptions, updated CLI architecture diagram, updated queue table columns
- Updated contracts.md: added full queue/settings/media_roots column listings, added exiftool/ffmpeg/ntfy as external dependencies, added tags to upload fields

## [0.1.7] - 2026-02-06

### Changed
- **Branding**: Lowercased app name from "Torrup" to "torrup" across entire codebase
  - `APP_NAME` config constant now "torrup"
  - `DEFAULT_RELEASE_GROUP` now "torrup"
  - Default `qbt_tag` setting now "torrup"
  - NFO templates now say "Uploaded with torrup"
  - CLI description, docstrings, Basic auth realm all lowercased
  - All fallback values in workers, CLI commands, and route handlers updated
  - Settings UI default values for release group and qBT tag lowercased
  - README, about.md, CONTRIBUTING.md, Dockerfile label updated
  - Tests updated to match new lowercase branding
  - 275 tests passing

## [0.1.6] - 2026-02-06

### Added
- **File Explorer**: Browse buttons on all path fields in Settings (Browse Base, Output Dir, Media Roots) that open a directory picker modal for navigating the filesystem
- **Theme Setting**: Light/Dark/System theme selector moved into Settings page (General section) with live preview; removed the header toggle button from all pages
- New `/api/browse-dirs` endpoint for server-side directory listing (skips hidden folders and symlinks)

### Changed
- Theme init script across all templates now supports "system" preference (was previously defaulting to a resolved value)

## [0.1.5] - 2026-02-06

### Changed
- **Crisp Design Language**: Converted all templates (index, queue, history, settings) from inline CSS with Iosevka font to Crisp design system (CrispByYosi font, external CSS, unified header/nav)
- **JS Extraction**: Moved queue and history page JavaScript into separate static files (static/js/queue.js, static/js/history.js) to keep templates under 400 lines

### Added
- **qBitTorrent Integration**:
    - Auto-seed: Automatically add uploaded torrents to qBitTorrent for seeding.
    - Auto-source: Monitor qBitTorrent completed downloads to auto-queue for upload.
    - Security: Support for `QBT_USER`, `QBT_PASS`, and `QBT_URL` environment variable overrides.
    - UI: "Test Connection" button and full settings management in the Web UI.
- **Worker Enhancements**:
    - `qbt_monitor_worker` for background qBitTorrent polling.
    - Case-insensitive category matching for automated workflows.
- **Tests**: New test suite for qBitTorrent utility functions (`tests/test_qbittorrent.py`).
 - **Testing**: `pytest.ini` to set `pythonpath=.` and exclude `reference/old-plugin` from test discovery.

## [0.1.4] - 2026-02-06

### Added
- Tracker module system (src/trackers/) - extracted TorrentLeech config into reusable tracker module
- Auto-scan worker (src/auto_worker.py) - background thread that periodically scans enabled media roots and queues missing content
- CLI scan command (src/cli/scan.py) - `torrup scan` for manual library scanning with duplicate detection
- Certainty scoring system - metadata quality scoring (0-100%) with automatic approval gating
- IMDB and TVMaze ID support in queue items and upload API
- Dashboard stats endpoint (GET /api/stats) with queue counts, automation status, last scan time
- System status panel on main page with live-updating stats
- Automation settings panel in settings UI (enable auto-scan, scan interval)
- Auto-scan checkbox per media root in settings
- IMDB/TVMaze metadata fields in queue edit modal (movies/tv only)
- generate_release_name() function for metadata-based release naming
- New DB columns: imdb, tvmazeid, tvmazetype, certainty_score, approval_status on queue table
- New DB columns: auto_scan, last_scan on media_roots table
- New settings: auto_scan_interval, enable_auto_upload

### Changed
- Upload API now accepts optional imdb, tvmazeid, tvmazetype parameters
- check_exists() now supports exact vs fuzzy search mode
- Queue worker only processes approved items (approval_status = 'approved')
- Queue list shows certainty percentage
- Branding updated from "Torrent uploader for TorrentLeech" to "Torrent Upload Tool"
- Category options moved from config.py to tracker module
- Routes split into routes.py + routes_queue.py for file size compliance
- Certainty scoring rebalanced: artist/album weighted highest, no format penalties
- Auto-scan worker now scans Artist/Album structure recursively for music
- Auto-scan uses fuzzy matching and rate limiting (1.5s between API calls)
- Auto-scan applies certainty scoring and approval gating
- Web UI queue add now uses generate_release_name() for music metadata-based naming
- Metadata extraction prioritizes FLAC over MP3 when both present
- Single exiftool call per file (eliminated redundant subprocess)

### Fixed
- Missing extract_metadata import in routes.py causing NameError on queue add
- Hardcoded /Volumes/media path in docker-compose.yml restored to env var
- Missing trailing newlines in db.py and cli/queue.py
- Worker now skips imdb/tvmazeid/tvmazetype for music uploads (movies/TV only)
- mktorrent FileNotFoundError now caught with install instructions instead of crash
- Mediainfo output now strips File name, Folder name, and absolute path lines (TL compliance)
- SQLite WAL mode enabled for concurrent access from web + worker + auto-scan
- Exiftool availability checked before use with clear warning if missing
- Auto-scan naming logic consolidated with generate_release_name() (was duplicated)

### Tests
- Split monolithic test_utils.py into focused test files: test_core.py, test_metadata.py, test_nfo.py, test_thumbnail.py, test_torrent.py
- Added tests for certainty scoring, release name generation, stats endpoint, IMDB/TVMaze validation
- Added tests for worker approval gate, music metadata guard, WAL mode, path stripping, exiftool check
- 262 tests passing

## [0.1.3] - 2026-02-04

### Fixed
- Corrected settings upsert SQL in `set_setting`
- NFO generation now captures mediainfo for single-file uploads
- Queue add now validates paths against enabled media roots and rejects symlinks/out-of-root paths

### Tests
- Added coverage for queue add path validation and updated queue-related route/db tests to use configured media roots

## [0.1.2] - 2026-02-04

### Changed
- Consolidated magazines media type into books (magazines removed as separate type)

### Docs
- Updated README.md and about.md to reflect v0.1.2 features (CLI, security, tests, metadata extraction)
- Removed deprecated basic auth documentation
- Updated platform support (macOS now planned, not current)

## [0.1.1] - 2026-02-03

### Added
- **CLI module** (src/cli.py) - 13 commands fully implemented (2026-02-03)
  - `torrup settings get/set` - configuration management
  - `torrup browse` - media library browsing
  - `torrup queue add/list/update/delete/run` - queue management
  - `torrup prepare/upload` - torrent preparation and upload
  - `torrup check-dup` - duplicate checking
  - `torrup uploads list/show` - upload history
- **GUI pages complete** - all 5 pages implemented (2026-02-03)
  - browse.html - media library browser with selection
  - queue.html - queue management with edit/delete/retry
  - history.html - upload history with filtering
- **Logging framework** (src/logger.py) - configurable logging (2026-02-03)
- **Health check endpoint** (/health) - database connectivity check (2026-02-03)
- **Page routes** - /browse, /queue, /history routes added (2026-02-03)
- NFO templates for each media type (movies, tv, music, books)
- Release group setting in config and settings UI
- NFO generation with templates, mediainfo, source/resolution extraction
- Metadata extraction using exiftool
- Thumbnail extraction using ffmpeg
- Settings for extract_metadata and extract_thumbnails
- thumb_path column in queue table

### Tests
- **206 passing tests** with **100% coverage** (2026-02-03)
  - test_db.py - 18 database tests
  - test_api.py - 9 Tracker API client tests (mocked)
  - test_routes.py - 44 endpoint tests
  - test_utils.py - 72 utility tests
  - test_worker.py - 10 worker tests

### Security
- SECRET_KEY now required - app fails fast if not set (2026-02-03)
- Added optional basic auth via TORRUP_AUTH_USER/TORRUP_AUTH_PASS (2026-02-03)
- Added security headers (X-Frame-Options, X-Content-Type-Options, etc.) (2026-02-03)
- Input validation for release names, categories, tags (2026-02-03)
- Path traversal prevention in file browser and torrent creation (2026-02-03)
- Error message sanitization - no internal paths or secrets exposed (2026-02-03)
- Disabled debug mode in production (2026-02-03)
- SQLite thread safety fix (2026-02-03)
- Reduced subprocess timeouts from 300s to 120s (2026-02-03)
- Announce URL format updated to `/a/<passkey>/announce` (2026-02-03)
- Escaped queue rendering to prevent XSS (2026-02-03)
- Added CSRF protection for POST endpoints (2026-02-03)

### Fixed
- Dockerfile now copies src/ directory (critical bug) (2026-02-03)
- Pinned base image to python:3.11.7-slim (2026-02-03)

### Tests
- Added basic pytest scaffold (routes + utils) (2026-02-03)

### Docs
- Added GUI specification at docs/gui/ - 4 files covering pages, API, design system, implementation phases (2026-02-03)
- Added comprehensive CLI reference at docs/CLI_REFERENCE.md - 13 commands fully documented (2026-02-03)
- Expanded techguide.md CLI section with architecture, exit codes, and command summaries (2026-02-03)
- SME: researched Docker repository best practices (2026-02-03)
- SME: researched GitHub repository best practices (2026-02-03)
- Added CODEOWNERS and dependabot.yml (2026-02-03)
- Added SUPPORT.md, updated SECURITY.md with contact, README with Contributing/License sections (2026-02-03)
- Updated README with security configuration (2026-02-03)
- Updated SECURITY.md with built-in protections documentation (2026-02-03)

## [0.1.0] - 2024-12-01

### Added
- Core Flask application with tracker API integration (supports TorrentLeech)
- Web UI for browsing media libraries and uploading torrents
- Queue system with background worker for batch uploads
- NFO generation using mediainfo
- Torrent creation using mktorrent (private flag, source tag)
- Duplicate detection via tracker search API
- Settings management UI (media roots, templates, categories)
- Docker containerization with Dockerfile
- Environment-based configuration

### Project Structure
- Split monolithic app.py into modules under src/
- Added about.md, contracts.md, techguide.md per project rules
- Added GitHub infrastructure (workflows, issue templates, PR template)
- Added LICENSE (MIT), CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
