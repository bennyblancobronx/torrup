# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2026-02-06

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
