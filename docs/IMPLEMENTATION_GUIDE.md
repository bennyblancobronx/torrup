# Torrup v0.1.x Implementation Guide

> Full audit completed 2026-02-03 | Target: Production-Ready v0.1.x

---

## Executive Summary

**Project**: Torrup - Torrent Upload Tool
**Current State**: Functionally complete, partially production-ready (needs test coverage + logging)
**Blocker Count**: 0 HIGH security, 0 MEDIUM security, tests present but coverage is minimal

### What Works
- Web UI (9 endpoints, all functional)
- Queue system (6 states: queued, preparing, uploading, success, failed, duplicate)
- Settings management (per-media-type configuration + qBitTorrent settings)
- Background worker (polling, state transitions, auto-seed to qBT)
- Auto-scan worker (periodic library scanning)
- qBitTorrent monitor (auto-source completed downloads)
- CLI (full command set: settings, browse, queue, scan, upload)
- Docker deployment (non-root user, health checks)
- Database layer (SQLite, parameterized queries)
- Tracker API integration (TorrentLeech search/upload)

### What's Missing
- Test coverage for complex scenarios (unit tests for core modules complete)

---

## Architecture Overview

```
Browser <-> Flask App (routes.py) <-> SQLite DB (db.py)
                |
                v
         Background Worker (worker.py)
                |
                v
    mediainfo + mktorrent + Tracker API (api.py)
```

### Source Files (778 lines total)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| src/config.py | 140 | Constants, env vars, NFO templates | COMPLETE |
| src/db.py | 134 | SQLite CRUD | COMPLETE |
| src/routes.py | 244 | Flask endpoints | COMPLETE |
| src/api.py | 59 | Tracker API Client (e.g. TorrentLeech) | COMPLETE |
| src/utils.py | 205 | NFO templates, torrent creation, metadata extraction | COMPLETE |
| src/worker.py | 100 | Queue processor | COMPLETE |
| app.py | 32 | Entry point | COMPLETE |

### External Dependencies

| Tool | Purpose | Required |
|------|---------|----------|
| mediainfo | Generate NFO metadata (technical specs) | Yes |
| mktorrent | Create .torrent files | Yes |
| curl | Health checks | Yes (Docker) |
| exiftool | Metadata extraction (titles, artists, albums, music tags) | Optional |
| ffmpeg/ffprobe | Thumbnail/artwork extraction + audio stream details | Optional |

---

## Implementation Phases

**Detailed steps in**: [IMPLEMENTATION_PHASES.md](IMPLEMENTATION_PHASES.md)

| Phase | Priority | Description |
|-------|----------|-------------|
| Phase 1 | COMPLETE | Security hardening (CSRF, XSS) |
| Phase 2 | BLOCKING | Expand test coverage (60% target) |
| Phase 3 | HIGH | Operational readiness (logging, health checks) |
| Phase 4 | MEDIUM | Documentation updates |
| Phase 5 | MEDIUM | Pre-release verification |

### Implementation Order

```
Week 1: Phase 1 (Security) + Phase 2.1-2.3 (Test structure)
Week 2: Phase 2.4-2.5 (Write tests, achieve 60% coverage)
Week 3: Phase 3 (Logging, health checks)
Week 4: Phase 4-5 (Documentation, verification, release)
```

---

## Issue Tracker

### BLOCKING (Must fix for v0.1.x)

| ID | Severity | File | Issue |
|----|----------|------|-------|
| TEST-001 | MEDIUM | tests/ | Minimal tests only; coverage needs expansion |

### RECOMMENDED (Should fix for v0.1.x)

| ID | Severity | File | Issue |
|----|----------|------|-------|
| OPS-001 | MEDIUM | - | No logging framework |
| OPS-002 | LOW | - | No dedicated health check endpoint |

### DEFERRED (v0.2.x+)

| ID | Feature | Notes |
|----|---------|-------|
| META-001 | IMDB/TVMaze lookups | Roadmap v0.2.x |
| DESK-001 | Desktop wrapper | Roadmap v0.3.x |
| TRACK-001 | Multi-tracker support | Extra trackers (e.g. IPT, RED) |

---

## Contracts Reference

### Tracker API (example: TorrentLeech)

| Endpoint | URL |
|----------|-----|
| Upload | `https://www.torrentleech.org/torrents/upload/apiupload` |
| Search | `https://www.torrentleech.org/api/torrentsearch` |
| Tracker | `https://tracker.torrentleech.org` |

**Announce URL format (TL):** `https://tracker.torrentleech.org/a/<passkey>/announce`

### Required Upload Fields (TL)

- `announcekey` - 32-char passkey
- `category` - Category number
- `torrent` - .torrent file
- `nfo` - NFO file

### Tracker Compliance (TL example)

- Torrent v1 only (no v2 or hybrid)
- Private flag must be set
- Source tag: `TorrentLeech.org`
- NFO required for every upload
- Announce URL must include passkey: `/a/<passkey>/announce`

---

## File Organization Rules

| Directory | Purpose |
|-----------|---------|
| /src | Source code |
| /tests | Test files |
| /docs | Documentation |
| /templates | HTML templates |
| /static | Static assets |
| /scripts | Utility scripts |

**Rules**:
- Never save to root folder
- Keep files under 400 lines
- No emojis in code or commits
- Test after every change

---

## Quick Commands

```bash
# Development
pip install -r requirements-dev.txt
export SECRET_KEY=dev-key-for-testing-only
python3 app.py

# Testing
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html

# Linting
black src/ app.py
isort src/ app.py
flake8 src/ app.py

# Docker
docker-compose up --build
docker-compose logs -f torrup

# Production
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
gunicorn -w 2 -b 0.0.0.0:5001 app:app
```

---

## Audit Sources

This guide reflects the current codebase, docs, and local TorrentLeech references.

**Last Updated**: 2026-02-03
