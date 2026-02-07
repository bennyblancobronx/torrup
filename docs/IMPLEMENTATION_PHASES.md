# Torrup v0.1.x - Implementation Phases

> Detailed implementation steps for each phase. See IMPLEMENTATION_GUIDE.md for overview.

---

## Phase 1: Security Hardening (BLOCKING)

**Priority**: CRITICAL - Must complete before any exposed deployment

### 1.1 Debug Mode Default (DONE)

**Status**: `app.py` now runs with `debug=False` by default.

### 1.2 Secret Key Enforcement (DONE)

**Status**: `SECRET_KEY` is required; app fails fast if unset.

### 1.3 Fix XSS in Message Field (MEDIUM) (DONE)

**File**: `templates/index.html:270`
**Current**:
```javascript
<td>${item.message || ''}</td>
```

**Fix**: Escape HTML entities before insertion
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
}
// Then use:
<td>${escapeHtml(item.message)}</td>
```

### 1.4 Add CSRF Protection (MEDIUM) (DONE)

**Install**: Add `Flask-WTF` to requirements.txt (done)

**File**: `app.py` - Add:
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

**Templates**: Add token to pages:
```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
```

**API Routes**: For AJAX, use header-based CSRF

### 1.5 Update .env.example (DONE)

```
# REQUIRED - Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=

# REQUIRED - Your tracker passkey (e.g. TorrentLeech 32 chars)
TL_ANNOUNCE_KEY=

# REQUIRED - Path to your media library
MEDIA_PATH=/path/to/your/media

# Optional - Set to "true" for development only
FLASK_DEBUG=false
```

---

## Phase 2: Test Suite (BLOCKING)

**Priority**: HIGH - Basic tests exist; expand coverage to 60%+

### Current State

- `tests/conftest.py` with test client fixture
- `tests/test_routes.py` (basic endpoint tests)
- `tests/test_utils.py` (basic utility tests)

### 2.1 Expand Test Structure

```
tests/
  conftest.py           # Fixtures (exists)
  test_routes.py        # Flask endpoint tests (exists)
  test_utils.py         # Utility function tests (exists)
  test_db.py            # Database CRUD tests (add)
  test_api.py           # Tracker API mock tests (add)
  test_worker.py        # Worker integration tests (add)
```

### 2.2 Update conftest.py (Fixtures)

```python
import importlib
import pytest

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("TORRUP_DB_PATH", str(tmp_path / "torrup.db"))
    monkeypatch.setenv("TORRUP_OUTPUT_DIR", str(tmp_path / "output"))
    monkeypatch.setenv("TORRUP_RUN_WORKER", "0")

    import src.config as config
    import src.db as db
    import app as app_module

    importlib.reload(config)
    importlib.reload(db)
    importlib.reload(app_module)

    app = app_module.app
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
```

### 2.3 Priority Test Files (Add)

**test_db.py** - Database operations (most critical)
- test_init_db_creates_tables
- test_get_setting_default
- test_set_setting
- test_add_queue_item
- test_update_queue_status
- test_delete_queue_item

**test_routes.py** - API endpoints
- test_index_returns_200
- test_browse_validates_media_type
- test_browse_prevents_traversal
- test_queue_add_requires_fields
- test_queue_list_returns_items

**test_utils.py** - Utility functions
- test_folder_size_calculation
- test_piece_size_selection
- test_release_name_sanitization
- test_path_exclusion_matching

### 2.4 Create requirements-dev.txt (DONE)

**Status**: `requirements-dev.txt` exists and matches the list below.

```
-r requirements.txt
black==24.1.0
isort==5.13.2
flake8==7.0.0
pytest==8.0.0
pytest-cov==4.1.0
```

### 2.5 Run Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Target**: 60% coverage minimum for v0.1.x

---

## Phase 3: Operational Readiness

### 3.1 Add Logging

**File**: `src/logger.py` (new)
```python
import logging
import os

def setup_logging():
    level = logging.DEBUG if os.environ.get("FLASK_DEBUG") == "true" else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger('tlt')

logger = setup_logging()
```

**Usage in worker.py**:
```python
from src.logger import logger

logger.info(f"Processing queue item {item['id']}")
logger.error(f"Upload failed: {str(e)}")
```

### 3.2 Add Health Check Endpoint

**File**: `src/routes.py` - Add:
```python
@bp.route('/health')
def health():
    """Health check endpoint for monitoring."""
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return jsonify({"status": "healthy", "version": "0.1.0"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503
```

### 3.3 Add Rate Limiting (Optional for v0.1.x)

**Install**: `Flask-Limiter`

```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per minute"])

@app.route('/api/browse')
@limiter.limit("30 per minute")
def browse():
    ...
```

---

## Phase 4: Documentation Updates

### 4.1 Update README.md

Add sections:
- Security configuration requirements
- Environment variables (required vs optional)
- Development setup with requirements-dev.txt
- Running tests

### 4.2 Update techguide.md

- Document new logging system
- Document health check endpoint
- Update security configuration

### 4.3 Update CHANGELOG.md

```markdown
## [0.1.1] - YYYY-MM-DD

### Security
- Added CSRF protection
- Fixed XSS in queue message display

### Added
- Test suite with 60%+ coverage
- Logging framework
- Health check endpoint

### Changed
- Announce URL format updated to /a/<passkey>/announce
```

---

## Phase 5: Pre-Release Checklist

### 5.1 Security Verification

```bash
# Run security scan
bandit -r src/ -ll

# Check for secrets
git secrets --scan

# Verify no debug mode
grep -r "debug=True" src/ app.py
```

### 5.2 Test Verification

```bash
# Run full test suite
pytest tests/ -v --cov=src --cov-fail-under=60

# Lint check
black --check src/ app.py
isort --check src/ app.py
flake8 src/ app.py
```

### 5.3 Docker Verification

```bash
# Build image
docker build -t torrup:0.1.1 .

# Test container
docker run -d -p 5001:5001 \
  -e SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))") \
  -e TL_ANNOUNCE_KEY=test \
  torrup:0.1.1

# Health check
curl http://localhost:5001/health
```

### 5.4 Manual Testing

- [ ] Add item to queue
- [ ] Browse media folders
- [ ] Update settings
- [ ] Delete queue item
- [ ] Verify path traversal blocked
- [ ] Verify 404 shows generic error (not stack trace)

---

## Phase 6: Metadata Extraction (COMPLETE)

**Status**: DONE - Implemented in v0.1.x

### 6.1 exiftool Integration (DONE)

Extracts embedded metadata from files:
- Movies/TV: title, year, description, show, season, episode
- Music: artist, album, track, year, genre
- Books: title, author, publisher, year, ISBN

Functions in `src/utils/metadata.py`:
- `extract_metadata(path, media_type)` - Returns normalized metadata dict
- `_find_primary_file(path, media_type)` - Finds best file to extract from
- `_normalize_metadata(raw, media_type)` - Standardizes exiftool output

### 6.2 ffmpeg/ffprobe Extraction (DONE)

Extracts visual assets and audio stream details:
- Video: Frame at 10% duration, scaled to 320px width
- Audio: Embedded album artwork
- Audio: Stream details via ffprobe (sample rate, bit depth, channels, bitrate)

Functions in `src/utils/metadata.py`:
- `extract_thumbnail(path, out_dir, release_name, media_type)`
- `_extract_video_thumbnail(video_path, out_path)`
- `_extract_album_art(audio_path, out_path)`
- `_audio_props_from_ffprobe(path)`

### 6.3 NFO Enhancement (DONE)

Metadata displayed in NFO files:
- Separate METADATA section before MEDIA INFO
- Fields formatted per media type
- Music: audio details, embedded/extracted artwork summary, local lyrics summary (when available)
- Falls back gracefully if extraction fails

### 6.4 Settings (DONE)

| Setting | Default | Description |
|---------|---------|-------------|
| `extract_metadata` | 1 | Enable exiftool extraction |
| `extract_thumbnails` | 1 | Enable ffmpeg extraction |

### 6.5 Database (DONE)

Added `thumb_path` column to queue table for tracking extracted thumbnails.
