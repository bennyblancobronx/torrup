# Torrup GUI Guide - API

API endpoints and response formats for the GUI.

---

## All Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (monitoring) |
| GET | `/api/stats` | Dashboard stats (queue counts, automation status) |
| GET | `/api/activity/health` | Current month activity health |
| GET | `/api/activity/history` | Monthly upload history (bar chart data) |
| GET | `/api/browse` | Browse media library folders |
| GET | `/api/browse-dirs` | Browse filesystem directories (for settings path picker) |
| GET | `/api/queue` | List all queue items |
| POST | `/api/queue/add` | Add items to queue |
| POST | `/api/queue/update` | Update a queue item |
| POST | `/api/queue/delete` | Delete a queue item |
| POST | `/api/settings` | Update application settings |
| POST | `/api/settings/qbt/test` | Test qBitTorrent connection |

---

## Page Routes

| Method | Route | Template | Description |
|--------|-------|----------|-------------|
| GET | `/` | `index.html` | Dashboard |
| GET | `/browse` | `browse.html` | Browse media library |
| GET | `/queue` | `queue.html` | Queue management |
| GET | `/history` | `history.html` | Upload history |
| GET | `/settings` | `settings.html` | Settings |

---

## Response Formats

### GET /health

Returns application health status.

```json
{
  "status": "healthy",
  "version": "0.1.8"
}
```

On failure returns HTTP 503:

```json
{
  "status": "unhealthy"
}
```

---

### GET /api/stats

Returns queue counts and automation status for the dashboard.

```json
{
  "queue_total": 12,
  "queue_pending": 5,
  "auto_enabled": true,
  "auto_interval": "60",
  "last_music_scan": "2026-02-03 14:32:15"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `queue_total` | int | Total items in queue |
| `queue_pending` | int | Items with status `queued` |
| `auto_enabled` | bool | Whether auto-scan/upload is enabled |
| `auto_interval` | string | Auto-scan interval in minutes |
| `last_music_scan` | string or null | Last scan timestamp for music root, or null if never scanned |

---

### GET /api/activity/health

Returns activity health status for the current month.

```json
{
  "uploads": 8,
  "queued": 3,
  "minimum": 10,
  "projected": 11,
  "needed": 0,
  "critical": false,
  "enforce": true,
  "days_remaining": 18,
  "pace": 1.14
}
```

| Field | Type | Description |
|-------|------|-------------|
| `uploads` | int | Successful/duplicate uploads this month |
| `queued` | int | Items currently queued |
| `minimum` | int | Configured monthly minimum |
| `projected` | int | uploads + queued |
| `needed` | int | How many more needed to meet minimum (0 if on track) |
| `critical` | bool | True if enforce is on and projected < minimum |
| `enforce` | bool | Whether activity enforcement is enabled |
| `days_remaining` | int | Days left in current month |
| `pace` | float or null | Uploads per day over last 7 days, null if zero |

**Rate limit:** 60 per minute

---

### GET /api/activity/history

Returns monthly upload counts for the bar chart.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `months` | int | 6 | Number of months to return (1-24) |

**Response:**

```json
[
  {"month": "2025-09", "count": 12},
  {"month": "2025-10", "count": 8},
  {"month": "2025-11", "count": 15},
  {"month": "2025-12", "count": 3},
  {"month": "2026-01", "count": 10},
  {"month": "2026-02", "count": 5}
]
```

Months with zero uploads are included. List is ordered chronologically.

**Rate limit:** 30 per minute

---

### GET /api/browse

Browse media library folders.

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `media_type` | string | no (default: `music`) | music, movies, tv, books |
| `path` | string | no | Absolute path to browse (defaults to media root) |

**Response:**

```json
{
  "root": "/media/music",
  "path": "/media/music/Artist Name/Album Name",
  "parent": "/media/music/Artist Name",
  "default_category": 31,
  "items": [
    {
      "name": "01 - Track.flac",
      "path": "/media/music/Artist Name/Album Name/01 - Track.flac",
      "is_dir": false,
      "size": "45.2 MB",
      "size_bytes": 47395430
    },
    {
      "name": "Subfolder",
      "path": "/media/music/Artist Name/Album Name/Subfolder",
      "is_dir": true,
      "size": "1.2 GB",
      "size_bytes": 1288490188
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `root` | string | Absolute path of the media root |
| `path` | string | Current absolute path being browsed |
| `parent` | string or null | Parent path, null if at media root |
| `default_category` | int | Default category ID for this media type |
| `items[].name` | string | File or folder name |
| `items[].path` | string | Absolute path |
| `items[].is_dir` | bool | Whether item is a directory |
| `items[].size` | string | Human-readable size, or "Too many files" on error |
| `items[].size_bytes` | int | Size in bytes, -1 if unable to calculate |

**Security:** Path traversal is blocked. Symlinks are rejected. Excluded folders are filtered out.

**Rate limit:** 60 per minute

---

### GET /api/browse-dirs

Browse filesystem directories for the settings path picker modal. Returns only directories (no files).

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | no (default: `/`) | Directory to list |

**Response:**

```json
{
  "path": "/media",
  "parent": "/",
  "dirs": [
    {"name": "music", "path": "/media/music"},
    {"name": "movies", "path": "/media/movies"}
  ]
}
```

**Security:** Path traversal blocked. Symlinks rejected. Hidden files (dot-prefixed) excluded.

**Rate limit:** 60 per minute

---

### GET /api/queue

List all queue items. Returns the full list; filtering is done client-side.

**Response:**

```json
[
  {
    "id": 45,
    "media_type": "movies",
    "path": "/media/movies/Movie.Name.2024",
    "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP",
    "category": 14,
    "tags": "1080p,BluRay",
    "imdb": "tt1234567",
    "tvmazeid": null,
    "tvmazetype": null,
    "status": "queued",
    "message": null,
    "tl_id": null,
    "created_at": "2026-02-03T14:00:00",
    "updated_at": "2026-02-03T14:00:00"
  }
]
```

Returns all columns from the `queue` table, ordered by ID descending.

---

### POST /api/queue/add

Add items to the upload queue.

**Request Body:**

```json
{
  "items": [
    {
      "media_type": "movies",
      "path": "/media/movies/Movie.Name.2024",
      "category": 14,
      "tags": "1080p,BluRay",
      "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP",
      "imdb": "tt1234567",
      "tvmazeid": "12345",
      "tvmazetype": "1"
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `media_type` | yes | One of: music, movies, tv, books |
| `path` | yes | Absolute path to the media item |
| `category` | yes | Valid category ID for the media type |
| `tags` | no | Comma-separated tags |
| `release_name` | no | Custom release name (auto-generated if omitted) |
| `imdb` | no | IMDB ID (format: tt1234567) |
| `tvmazeid` | no | TVMaze show ID |
| `tvmazetype` | no | TVMaze type (1 or 2) |

If `extract_metadata` setting is enabled and no release_name is provided, the server will attempt to extract metadata and generate a release name automatically.

**Response:**

```json
{
  "success": true,
  "ids": [45]
}
```

**Rate limit:** 10 per minute

---

### POST /api/queue/update

Update a queue item. Only provided fields are updated.

**Request Body:**

```json
{
  "id": 45,
  "release_name": "New.Release.Name-GROUP",
  "category": 14,
  "tags": "1080p,BluRay,x264",
  "status": "queued",
  "imdb": "tt1234567",
  "tvmazeid": "12345",
  "tvmazetype": "1"
}
```

| Field | Required | Validation |
|-------|----------|------------|
| `id` | yes | Must be valid integer |
| `release_name` | no | No path traversal characters |
| `category` | no | Must be valid integer |
| `tags` | no | Alphanumeric, commas, spaces, hyphens only |
| `status` | no | One of: queued, preparing, uploading, success, failed, duplicate |
| `imdb` | no | Format: `tt` + 7-9 digits |
| `tvmazeid` | no | Digits only |
| `tvmazetype` | no | `1` or `2` |

**Response:**

```json
{
  "success": true
}
```

**Rate limit:** 30 per minute

---

### POST /api/queue/delete

Delete a queue item.

**Request Body:**

```json
{
  "id": 45
}
```

**Response:**

```json
{
  "success": true
}
```

**Rate limit:** 20 per minute

---

### POST /api/settings

Update application settings. Only provided fields are updated.

**Request Body:**

```json
{
  "output_dir": "/app/output",
  "release_group": "torrup",
  "exclude_dirs": "torrents,downloads,tmp,trash",
  "test_mode": "0",
  "extract_metadata": "1",
  "extract_thumbnails": "1",
  "enable_auto_upload": "0",
  "auto_scan_interval": "60",
  "qbt_enabled": "0",
  "qbt_url": "http://localhost:8080",
  "qbt_user": "admin",
  "qbt_pass": "adminadmin",
  "tl_min_uploads_per_month": "10",
  "tl_min_seed_copies": "10",
  "tl_min_seed_days": "7",
  "tl_inactivity_warning_weeks": "3",
  "tl_absence_notice_weeks": "4",
  "tl_enforce_activity": "1",
  "ntfy_enabled": "0",
  "ntfy_url": "https://ntfy.sh",
  "ntfy_topic": "torrup-alerts",
  "media_roots": [
    {
      "media_type": "music",
      "enabled": true,
      "auto_scan": true,
      "path": "/media/music",
      "default_category": 31
    }
  ],
  "templates": {
    "music": "Artist.Album.Source.Codec-Group",
    "movies": "Name.Year.Resolution.Source.Codec-Group"
  }
}
```

**Accepted Setting Keys:**

| Category | Keys |
|----------|------|
| General | `output_dir`, `exclude_dirs`, `release_group` |
| Automation | `test_mode`, `enable_auto_upload`, `auto_scan_interval` |
| Metadata | `extract_metadata`, `extract_thumbnails` |
| qBitTorrent | `qbt_enabled`, `qbt_url`, `qbt_user`, `qbt_pass` |
| TorrentLeech | `tl_min_uploads_per_month`, `tl_min_seed_copies`, `tl_min_seed_days`, `tl_inactivity_warning_weeks`, `tl_absence_notice_weeks`, `tl_enforce_activity` |
| Notifications | `ntfy_enabled`, `ntfy_url`, `ntfy_topic` |
| Media Roots | `media_roots` array (per media type: path, enabled, default_category, auto_scan) |
| Templates | `templates` object (per media type: naming pattern string) |

**Response:**

```json
{
  "success": true
}
```

**Rate limit:** 5 per minute

---

### POST /api/settings/qbt/test

Test connection to qBitTorrent using current settings.

**Response (success):**

```json
{
  "success": true,
  "version": "4.6.2"
}
```

**Response (failure):**

```json
{
  "success": false,
  "error": "Failed to connect. Check logs or settings."
}
```

**Rate limit:** 5 per minute

---

## CSRF Protection

All POST endpoints require a CSRF token. The token is set via a `<meta>` tag in each template:

```html
<meta name="csrf-token" content="{{ csrf_token() }}" />
```

JavaScript sends it in the `X-CSRFToken` header on POST requests.

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": "Description of what went wrong"
}
```

Some endpoints also use `{"success": false, "error": "..."}`.

HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters, disabled media type) |
| 403 | Access denied (path traversal, symlinks) |
| 404 | Resource not found |
| 500 | Server error |
| 503 | Service unavailable (health check failure) |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [Pages](pages.md) - Page wireframes and components
- [Implementation](implementation.md) - File structure and build info
