# Torrup GUI Guide - API

API endpoints and response formats for the GUI.

---

## Existing Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/browse` | Browse media folders |
| GET | `/api/queue` | List queue items |
| POST | `/api/queue/add` | Add items to queue |
| POST | `/api/queue/update` | Update queue item |
| POST | `/api/queue/delete` | Delete queue item |
| POST | `/api/settings` | Update settings |

---

## New Endpoints Needed

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Dashboard stats (counts by status) |
| GET | `/api/system` | System status (worker, deps, db) |
| GET | `/api/history` | Upload history list |
| GET | `/api/activity` | Activity log |

---

## Response Formats

### GET /api/stats

Returns queue item counts grouped by status.

```json
{
  "queued": 12,
  "preparing": 0,
  "uploading": 2,
  "success": 156,
  "failed": 3,
  "duplicate": 5
}
```

---

### GET /api/system

Returns system health and configuration status.

```json
{
  "worker": {
    "running": true,
    "pid": 1234
  },
  "dependencies": {
    "mediainfo": true,
    "mktorrent": true
  },
  "api_key": {
    "configured": true
  },
  "database": {
    "path": "/app/torrup.db",
    "size_bytes": 159744
  }
}
```

---

### GET /api/history

Returns completed uploads with optional filters.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | string | all | Filter by status (success, failed, duplicate) |
| `media_type` | string | all | Filter by media type |
| `limit` | int | 50 | Max items to return |
| `offset` | int | 0 | Pagination offset |
| `since` | string | - | ISO date, items after this date |

**Response:**

```json
{
  "items": [
    {
      "id": 42,
      "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP",
      "media_type": "movies",
      "category": 14,
      "tags": "1080p,BluRay",
      "status": "success",
      "tracker_id": 1234567,
      "created_at": "2026-02-03T14:32:15Z",
      "torrent_path": "/app/output/Movie.Name.2024.torrent",
      "nfo_path": "/app/output/Movie.Name.2024.nfo"
    }
  ],
  "total": 156,
  "limit": 50,
  "offset": 0
}
```

---

### GET /api/activity

Returns timestamped activity log.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 100 | Max items to return |
| `offset` | int | 0 | Pagination offset |
| `since` | string | - | ISO date, items after this date |

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "timestamp": "2026-02-03T14:32:15Z",
      "action": "upload_success",
      "queue_id": 42,
      "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP",
      "details": "Tracker ID: 1234567"
    },
    {
      "id": 2,
      "timestamp": "2026-02-03T14:30:00Z",
      "action": "queue_add",
      "queue_id": 42,
      "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP",
      "details": null
    }
  ],
  "total": 500,
  "limit": 100,
  "offset": 0
}
```

**Action Types:**

| Action | Description |
|--------|-------------|
| `queue_add` | Item added to queue |
| `queue_update` | Item details updated |
| `queue_delete` | Item removed from queue |
| `upload_start` | Upload process started |
| `upload_success` | Upload completed successfully |
| `upload_failed` | Upload failed |
| `duplicate_found` | Duplicate detected |

---

### GET /api/browse

Browse media library folders.

**Query Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `media_type` | string | yes | music, movies, tv, books |
| `path` | string | no | Subdirectory path (relative to media root) |

**Response:**

```json
{
  "root": "/media/music",
  "path": "Artist Name/Album Name",
  "parent": "Artist Name",
  "default_category": 31,
  "items": [
    {
      "name": "01 - Track.flac",
      "path": "Artist Name/Album Name/01 - Track.flac",
      "is_dir": false,
      "size": "45.2 MB"
    },
    {
      "name": "Subfolder",
      "path": "Artist Name/Album Name/Subfolder",
      "is_dir": true,
      "size": "--"
    }
  ]
}
```

---

### GET /api/queue

List queue items.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | string | all | Filter by status |
| `media_type` | string | all | Filter by media type |
| `limit` | int | 50 | Max items to return |

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
    "status": "queued",
    "message": null,
    "created_at": "2026-02-03T14:00:00Z",
    "updated_at": "2026-02-03T14:00:00Z"
  }
]
```

---

### POST /api/queue/add

Add items to queue.

**Request Body:**

```json
{
  "items": [
    {
      "media_type": "movies",
      "path": "/media/movies/Movie.Name.2024",
      "category": 14,
      "tags": "1080p,BluRay",
      "release_name": "Movie.Name.2024.1080p.BluRay.x264-GROUP"
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "added": 1,
  "ids": [45]
}
```

---

### POST /api/queue/update

Update a queue item.

**Request Body:**

```json
{
  "id": 45,
  "release_name": "New.Release.Name-GROUP",
  "category": 14,
  "tags": "1080p,BluRay,x264"
}
```

**Response:**

```json
{
  "success": true
}
```

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

---

### POST /api/settings

Update application settings.

**Request Body:**

```json
{
  "browse_base": "/media",
  "output_dir": "/app/output",
  "exclude_dirs": "torrents,downloads,tmp,trash",
  "media_roots": [
    {
      "media_type": "music",
      "enabled": true,
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

**Response:**

```json
{
  "success": true
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Description of what went wrong"
}
```

HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | Resource not found |
| 500 | Server error |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [Pages](pages.md) - Page wireframes and components
- [Implementation](implementation.md) - Phases and file structure
