# Docker Production Audit -- Torrup v0.1.4

## Problem

Torrup is a single-container Docker image. All external tools (mktorrent, mediainfo, exiftool, ffmpeg) are installed at build time. The current Docker setup has gaps that range from broken UI to missing security hardening.

## Design Decisions (Non-Negotiable)

- **No startup dependency kills.** Commit b282793 deliberately removed these. The app works without mktorrent/mediainfo for browsing, settings, and queue management. Runtime errors at point of use are correct.
- **No self-heal apt-get at runtime.** The container runs as non-root (appuser). apt-get requires root. The apt cache is deleted. If tools are missing, the image is broken and must be rebuilt.
- **Workers = 1.** SQLite does not support concurrent writers. Background daemon threads (queue_worker, auto_scan_worker) share the process. Multiple workers = duplicate threads + SQLite lock contention.

---

## TIER 1 -- BROKEN (will cause failures)

### Fix 1: static/ directory not copied into image

**File:** `Dockerfile` line 22-24
**What:** Copies app.py, src/, templates/ but not static/. CSS and fonts return 404. UI is completely unstyled.
**Confirmed:** static/ has 7 files (2 CSS, 5 woff2 fonts). Templates reference them via `url_for('static', ...)`.
**Fix:** Add `COPY --chown=appuser:appuser static ./static/` after the templates copy.

### Fix 2: HEALTHCHECK hits wrong endpoint (long-term: robust healthcheck)

**File:** `Dockerfile` line 38, `docker-compose.yml` line 23
**What:** Both hit `http://localhost:5001/` (index page) instead of `/health`. Problems:
- Index returns HTML, not a meaningful health signal
- If basic auth is enabled (TORRUP_AUTH_USER/PASS set), healthcheck gets 401 every time = container restart loop
- Database failures go undetected (index doesn't test DB, /health does)
**Fix (long-term):** Change both to `http://localhost:5001/health` and add explicit healthcheck timing in `docker-compose.yml`:
```yaml
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:5001/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 60s
```

### Fix 3: Templates volume mount breaks portable deployment

**File:** `docker-compose.yml` line 19
**What:** `./templates:/app/templates:ro` overlays local templates over baked-in image templates. If user has no local templates/ directory, container serves broken UI or errors.
**Fix:** Remove the line. Templates are baked into the image at build time.

### Fix 4: Gunicorn timeout kills long operations (long-term: configurable)

**File:** `Dockerfile` line 40
**What:** No explicit timeout (defaults to 30s). But `create_torrent()` has a 120s subprocess timeout (torrent.py:75) and `mediainfo` has 30s (nfo.py:44). Gunicorn kills the worker at 30s, leaving queue items stuck in "preparing" or "uploading" status permanently.
**Fix (long-term):** Add `--timeout 180` to the gunicorn CMD, but make it configurable with `TORRUP_GUNICORN_TIMEOUT` env var (default 180). This keeps headroom over the 120s mktorrent timeout while allowing site-specific tuning.

---

## TIER 2 -- WRONG (incorrect, won't crash)

### Fix 5: APP_VERSION stale

**File:** `src/config.py` line 9
**What:** Says `0.1.2`. Current version is `0.1.4`.
**Fix:** Change to `APP_VERSION = "0.1.4"`.

### Fix 6: Dockerfile labels outdated

**File:** `Dockerfile` lines 3-5
**What:** Version `0.1.0`, description says "Torrent uploader for TorrentLeech". Both wrong.
**Fix:** Update to `version="0.1.4"` and `description="Torrup - Torrent Upload Tool"`.

### Fix 7: Error messages reference host installs from inside container

**File:** `src/utils/torrent.py` lines 81-83
**What:** Says "Install with: brew install mktorrent (macOS) or apt install mktorrent (Linux)". User is inside Docker.
**Fix:** Change to `"mktorrent not found -- container may need rebuild"`.

**File:** `src/utils/nfo.py` line 57
**What:** Silently sets fallback `"  MediaInfo not available"` with no log output.
**Fix:** Add `logger.warning("mediainfo binary not found -- container may need rebuild")` before the fallback.

### Fix 8: app.py docstring stale branding

**File:** `app.py` lines 2-3
**What:** Says "Torrent uploader for TorrentLeech". Should match rebranding.
**Fix:** Change to `"Torrup - Torrent Upload Tool"`.

---

## TIER 3 -- MISSING (best practice gaps)

### Fix 9: No request concurrency (long-term: safe concurrency)

**File:** `Dockerfile` line 40
**What:** Single sync worker handles one request at a time. Any long request (browsing large directory, torrent creation) blocks all other requests including health checks.
**Fix (long-term):** Prefer `--worker-class gthread --threads 4` in a single worker process, but only after verifying thread-safety of DB connections and any global state. If thread-safety is uncertain, keep sync workers and move long-running tasks to the queue worker (or a dedicated background process) to preserve responsiveness without in-process threading.

### Fix 10: No graceful shutdown for background threads (long-term: clean lifecycle)

**Files:** `app.py`, `src/worker.py`, `src/auto_worker.py`
**What:** Background threads use `while True` + `time.sleep()`. When Docker sends SIGTERM, gunicorn shuts down but daemon threads are killed instantly. Queue items left in "uploading" status permanently.
**Fix (long-term):** Add a `threading.Event` shutdown signal in app.py. Workers check `shutdown_event.is_set()` instead of `while True`, and use `shutdown_event.wait(N)` instead of `time.sleep(N)`. Also set `stop_grace_period` to match worst-case upload durations to avoid SIGKILL.

Changes:
- `app.py`: Create `shutdown_event = threading.Event()`, register SIGTERM/SIGINT handlers that set it, pass to workers
- `src/worker.py` line 158: `while True` -> `while not shutdown_event.is_set()`, line 167: `time.sleep(2)` -> `shutdown_event.wait(2)`
- `src/auto_worker.py` line 26: `while True` -> `while not shutdown_event.is_set()`, lines 34/58/62: `time.sleep()` -> `shutdown_event.wait()`

### Fix 11: Security hardening in docker-compose (long-term: least privilege)

**File:** `docker-compose.yml`
**What:** Container runs with full Linux capabilities and writable filesystem. Unnecessary for this app.
**Fix (long-term):** Add:
```yaml
    read_only: true
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp
```
Ensure all writes are confined to `/app/data`, `/app/output`, and `/tmp` (set `TMPDIR=/tmp`). If other paths are required, document them and mount as volumes.

### Fix 12: No resource limits (long-term: enforceable limits)

**File:** `docker-compose.yml`
**What:** No memory/CPU limits. mktorrent and ffmpeg on large files can consume all host resources.
**Fix (long-term):** Add:
```yaml
    mem_limit: 1g
    cpus: '2.0'
```
Document that strict enforcement depends on the runtime; for hardened production, use a scheduler (Swarm/K8s) with explicit resource limits.

### Fix 13: No log rotation (long-term: consistent logging)

**File:** `docker-compose.yml`
**What:** No logging driver config. Logs grow unbounded.
**Fix (long-term):** Add:
```yaml
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```
Also set `PYTHONUNBUFFERED=1` in the Dockerfile so logs are not buffered.

### Fix 14: No stop grace period (long-term: match workloads)

**File:** `docker-compose.yml`
**What:** Default is 10s. Tracker uploads can take 30+s. Workers get SIGKILL mid-upload.
**Fix (long-term):** Add `stop_grace_period: 60s` (or higher, based on worst-case upload/ffmpeg durations).

### Fix 15: COPY --chown instead of chown -R layer (long-term: lean image)

**File:** `Dockerfile`
**What:** Current pattern copies files as root then runs `chown -R appuser:appuser /app`, which duplicates all file data in a separate layer. Using `COPY --chown` avoids the extra layer.
**Fix:** Restructure COPY commands:
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
RUN mkdir -p /app/data /app/output && chown appuser:appuser /app /app/data /app/output
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
USER appuser
COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser src ./src/
COPY --chown=appuser:appuser templates ./templates/
COPY --chown=appuser:appuser static ./static/
```

### Fix 16: Gunicorn access logging (long-term: observability)

**File:** `Dockerfile` line 40
**What:** No access log. Hard to debug production issues.
**Fix (long-term):** Add `--access-logfile -` to gunicorn CMD (logs to stdout, captured by Docker). Optionally allow `TORRUP_GUNICORN_ACCESS_LOG` to disable access logs in low-noise deployments.

---

## Files to modify

| # | File | Changes |
|---|------|---------|
| 1 | `Dockerfile` | Add static/ copy, fix HEALTHCHECK, update labels, restructure COPY --chown, update CMD with gthread/timeout/threads/access-log |
| 2 | `docker-compose.yml` | Remove templates volume, fix healthcheck URL, add security hardening, resource limits, log rotation, stop_grace_period |
| 3 | `app.py` | Add shutdown_event + signal handlers, pass to workers, fix docstring |
| 4 | `src/worker.py` | Replace while True / time.sleep with shutdown_event checks |
| 5 | `src/auto_worker.py` | Replace while True / time.sleep with shutdown_event checks |
| 6 | `src/utils/torrent.py` | Fix error message for Docker context |
| 7 | `src/utils/nfo.py` | Add logger.warning for missing mediainfo |
| 8 | `src/config.py` | Version bump to 0.1.4 |

## NOT changing (deliberate omissions)

| Item | Reason |
|------|--------|
| Startup dependency checks | Deliberately removed in b282793. App works without tools for browsing/settings/queue. |
| Self-heal apt-get at runtime | Runs as non-root. apt cache deleted. Anti-pattern in containers. |
| Health endpoint dep checks | Tools guaranteed by Dockerfile. shutil.which() on every 30s probe is wasted work. |
| Multi-stage build | Pure savings ~30MB. Not worth the complexity for this project. |
| File-based secrets | Env vars + .env file is fine for single-host personal deployment. |
| Gunicorn workers > 1 | SQLite + daemon threads. Must stay at 1. |
| nginx for static files | 7 small files, single-user tool. Flask serving is fine. |

## Verification

1. `python -m pytest tests/ -q` -- all tests pass
2. `docker build -t torrup .` -- builds clean
3. `docker compose up -d` -- starts without errors
4. `curl http://localhost:5001/health` -- returns `{"status":"healthy","version":"0.1.4"}`
5. `curl http://localhost:5001/` -- page loads with CSS/fonts
6. `docker stop torrup` -- workers log graceful shutdown within 60s
7. `docker inspect torrup` -- verify labels, healthcheck, security opts
