# Torrup GUI Guide - Pages

Wireframes and component specifications for each page.

---

## Page 1: Dashboard

**Route:** `/`
**Template:** `index.html`
**Script:** `static/js/dashboard.js`
**Purpose:** Combined view with stats, browse library, inline queue management, and activity chart

### Wireframe

```
+---------------------------------------------------------------------+
| DASHBOARD                                                            |
+---------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | ACTIVITY WARNING (conditional, red left border)                  |
|  |  Projected uploads: 4 / 10. Need 6 more in 18 days. Pace: 0.5/d |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | SYSTEM STATUS                                                    |
|  |  +-----------+  +-------------+  +-----------------+             |
|  |  | Queue     |  | Automation  |  | Last Music Scan |             |
|  |  | 12        |  | On          |  | 2026-02-03      |             |
|  |  | 5 pending |  | Interval:60m|  | 14:32:15        |             |
|  |  +-----------+  +-------------+  +-----------------+             |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | MONTHLY UPLOADS (last 6 months)     (bar chart)                  |
|  |  [===]  [====]  [======]  [========]  [===]  [==]                |
|  |   08     09      10        11          12     01                 |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | BROWSE LIBRARY                                                   |
|  |  Media type: [Music v]  [Refresh]                                |
|  |  [root] [.. (up)] path/to/current                                |
|  |  +--------------------------------------------------------------+|
|  |  | [x] folder-name-1                              1.2 GB        ||
|  |  | [ ] folder-name-2                              450 MB        ||
|  |  | [ ] file.flac                                  32 MB         ||
|  |  +--------------------------------------------------------------+|
|  |  [Add Selected to Queue]  0 selected                             |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | QUEUE                                            [Reload]        |
|  |  ID | Type  | Release Name    | Cat   | Tags | Status | Msg | Act|
|  |  45 | music | [editable     ] | [v  ] | [  ] | queued |     |S|D||
|  +------------------------------------------------------------------+
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Activity Warning** | `.card` with red left border | Conditional banner when projected uploads < minimum |
| **Stat Cards** | `.card .stat-card` | 3 cards: Queue count, Automation on/off, Last Music Scan |
| **Monthly Chart** | `.card` | Bar chart from `/api/activity/history`, hidden if no data |
| **Browse Library** | `.card` | Media type dropdown, breadcrumb nav, file list with checkboxes |
| **Queue Table** | `.card .table` | Inline editable queue with save/delete per row |

### Data Sources

| Data | Source |
|------|--------|
| System stats | `GET /api/stats` (auto-refreshes every 30s) |
| Activity health | `GET /api/activity/health` (auto-refreshes every 60s) |
| Monthly chart | `GET /api/activity/history?months=6` |
| Directory listing | `GET /api/browse?media_type=X&path=Y` |
| Queue list | `GET /api/queue` |

---

## Page 2: Browse

**Route:** `/browse`
**Template:** `browse.html`
**Script:** `static/js/browse.js`
**Purpose:** Dedicated media library browser with select-all and size tracking

### Wireframe

```
+---------------------------------------------------------------------+
| BROWSE LIBRARY                                                       |
+---------------------------------------------------------------------+
|                                                                      |
|  Media Type: [Music v]    [Refresh]                                 |
|                                                                      |
|  [Home]  [Up One Level]  path/to/current                            |
|                                                                      |
|  +------------------------------------------------------------------+
|  | [x]  NAME                                              SIZE      |
|  +------------------------------------------------------------------+
|  | [x]  [D] Subfolder A                                   --        |
|  | [ ]  [D] Subfolder B                                   --        |
|  | [x]  [D] Album.Name.2024.FLAC                          1.2 GB    |
|  +------------------------------------------------------------------+
|                                                                      |
|  Selected: 2 items  |  1.65 GB                                      |
|                                                                      |
|  [Add to Queue]                                                     |
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Media Type Dropdown** | `.input` (select) | music, movies, tv, books (non-music disabled as "coming soon") |
| **Breadcrumb** | `.path-nav .breadcrumb` | Current path with clickable segments |
| **Navigation Buttons** | `.btn-ghost` | Home (root) and Up (parent directory) |
| **Select All** | checkbox | Toggle all items in current directory |
| **File List** | `.table` | Checkbox, type icon, name (clickable for dirs), size |
| **Selection Summary** | `.text-secondary` | Count and total size of selected items |
| **Add to Queue** | `.btn-primary` | Primary action button, redirects to queue page |

### Interactions

| Action | Result |
|--------|--------|
| Click folder name | Navigate into folder |
| Click checkbox | Toggle selection |
| Click Select All | Toggle all items |
| Change media type | Reset to root of that media type |
| Click Home | Return to media root |
| Click Up | Go to parent directory |
| Click Add to Queue | POST items, redirect to Queue page |

### Data Sources

| Data | Source |
|------|--------|
| Directory listing | `GET /api/browse?media_type=X&path=Y` |
| Add items | `POST /api/queue/add` |

---

## Page 3: Queue

**Route:** `/queue`
**Template:** `queue.html`
**Script:** `static/js/queue.js`
**Purpose:** Manage pending and active uploads with filtering and inline editing

### Wireframe

```
+---------------------------------------------------------------------+
| UPLOAD QUEUE                                                         |
+---------------------------------------------------------------------+
|                                                                      |
|  [All] [Queued] [Uploading] [Failed]    [x] Auto-refresh  [Refresh] |
|                                                                      |
|  +------------------------------------------------------------------+
|  | ID  | TYPE   | RELEASE NAME           | CAT  | STATUS | ACT     |
|  +------------------------------------------------------------------+
|  | 45  | movies | Movie.Name.2024...     | 14   | queued | [E][X]  |
|  | 44  | music  | Album.Name.FLAC...     | 31   | upload | [--]    |
|  | 43  | tv     | Show.S01E01...         | 26   | failed | [R][X]  |
|  | 42  | books  | Book.Title.2024...     | 45   | success| [V]     |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | EDIT ITEM #45                                                    |
|  |                                                                  |
|  |  Release Name: [Movie.Name.2024.1080p.BluRay.x264-GROUP        ]|
|  |  Category:     [Movies :: BlurayRip v]                          |
|  |  Tags:         [1080p, BluRay, x264                            ]|
|  |  IMDB:         [tt1234567                                      ]|
|  |  TVMaze ID:    [12345                                          ]|
|  |                                                                  |
|  |  [Save Changes]  [Cancel]                                       |
|  +------------------------------------------------------------------+
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Filter Tabs** | `.filter-tabs .tab` | All, Queued, Uploading, Failed quick filters |
| **Auto-refresh** | `.auto-refresh` checkbox | Toggle periodic queue reload |
| **Queue Table** | `.table` | ID, type, release name, category, status, actions |
| **Action Buttons** | `.btn-ghost .btn-sm` | Edit, Delete, Retry, View |
| **Edit Panel** | `.card` | Expandable form for editing item details |

### Status Actions

| Status | Available Actions |
|--------|-------------------|
| `queued` | Edit, Delete |
| `preparing` | View (read-only) |
| `uploading` | View (read-only) |
| `success` | View details |
| `failed` | Retry, Edit, Delete |
| `duplicate` | View, Delete |

### Editable Fields

| Field | Validation |
|-------|------------|
| `release_name` | No path traversal (`..`, `/`, `\`) |
| `category` | Must be valid int for the media type |
| `tags` | Alphanumeric, commas, spaces, hyphens only |
| `status` | Must be one of: queued, preparing, uploading, success, failed, duplicate |
| `imdb` | Format: `tt` followed by 7-9 digits |
| `tvmazeid` | Numeric only |
| `tvmazetype` | `1` or `2` only |

### Data Sources

| Data | Source |
|------|--------|
| Queue list | `GET /api/queue` |
| Update item | `POST /api/queue/update` |
| Delete item | `POST /api/queue/delete` |

---

## Page 4: History

**Route:** `/history`
**Template:** `history.html`
**Script:** `static/js/history.js`
**Purpose:** View past uploads and activity log derived from queue data

### Wireframe

```
+---------------------------------------------------------------------+
| UPLOAD HISTORY                           This month: 8 / 10         |
+---------------------------------------------------------------------+
|                                                                      |
|  Tabs: [Uploads] [Activity]                                         |
|                                                                      |
|  Filter: [All v]  Date: [Last 7 days v]  Type: [All v]  [Refresh]  |
|                                                                      |
|  +------------------------------------------------------------------+
|  | DATE       | RELEASE NAME               | STATUS | TL ID         |
|  +------------------------------------------------------------------+
|  | 2026-02-03 | Movie.Name.2024.1080p...   | OK     | #1234567     |
|  | 2026-02-03 | Album.FLAC.2024...         | OK     | #1234566     |
|  | 2026-02-02 | Show.S01E01...             | DUP    | --           |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | DETAILS: Movie.Name.2024.1080p.BluRay.x264-GROUP                 |
|  |                                                                  |
|  |  TL ID:            #1234567                                      |
|  |  Category:         Movies :: BlurayRip                          |
|  |  Tags:             1080p, BluRay                                |
|  |  Timestamp:        2026-02-03 14:32:15                          |
|  |  Path:             /media/movies/Movie.Name.2024                |
|  |                                                                  |
|  |  Files Generated:                                               |
|  |    OK  Movie.Name.2024.torrent                                  |
|  |    OK  Movie.Name.2024.nfo                                      |
|  |    OK  Movie.Name.2024.xml                                      |
|  +------------------------------------------------------------------+
+---------------------------------------------------------------------+
```

### Tabs

| Tab | Content |
|-----|---------|
| **Uploads** | Queue items filtered to success/failed/duplicate statuses, with details panel |
| **Activity** | Timestamped log derived from the same queue data (status as action type) |

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Monthly Counter** | `.text-muted` | "This month: X / Y" from activity health API |
| **Tab Switcher** | `.tab` | Toggle between Uploads and Activity views |
| **Filters** | `.input` (select) | Status, date range (7/30/90 days or all), media type |
| **History Table** | `.table` | Date, release name, status badge, TL ID |
| **Details Panel** | `.details-panel` | Click row to show: TL ID, category, tags, timestamp, path, generated files |
| **Activity Log** | `.activity-item` | Timestamp, action (status), message per entry |

### Data Sources

| Data | Source | Notes |
|------|--------|-------|
| Upload history | `GET /api/queue` | Client-side filtered to success/failed/duplicate |
| Monthly counter | `GET /api/activity/health` | Shows uploads vs minimum for current month |

Note: There is no dedicated `/api/history` or `/api/activity` endpoint. The history page fetches all queue items via `GET /api/queue` and filters them client-side by status. The activity tab is also derived from the same queue data.

---

## Page 5: Settings

**Route:** `/settings`
**Template:** `settings.html`
**Script:** `static/js/settings.js`
**Purpose:** Configure all application settings

### Wireframe

```
+---------------------------------------------------------------------+
| SETTINGS                                                             |
+---------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | GENERAL                                                          |
|  |  Output Dir:        [/app/output              ] [Browse]         |
|  |  Release Group:     [torrup                    ]                 |
|  |  Exclude Folders:   [torrents,downloads,tmp    ]                 |
|  |  Theme:             [System Default v]                           |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | AUTOMATION (Beta)                                                |
|  |  [x] Test Mode (Dry Run)                                        |
|  |  [x] Enable Auto-Scan + Upload                                  |
|  |  Scan Interval (minutes): [60]                                   |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | MEDIA ROOTS + DEFAULTS                                           |
|  |  TYPE   | ENABLED | AUTO SCAN | PATH            | CATEGORY      |
|  |  music  | [x]     | [x]       | [/media/music  ]| [Audio v]     |
|  |  movies | [ ]     | [ ]       | [/media/movies ] | (coming soon) |
|  |  tv     | [ ]     | [ ]       | [/media/tv     ] | (coming soon) |
|  |  books  | [ ]     | [ ]       | [/media/books  ] | (coming soon) |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | METADATA EXTRACTION                                              |
|  |  [x] Extract Metadata (exiftool)                                |
|  |  [x] Extract Thumbnails (ffmpeg)                                |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | QBITTORRENT INTEGRATION                                         |
|  |  [x] Enable qBitTorrent    [x] Auto-Add to qBT    qBT Tag: []  |
|  |  [x] Auto-Source from qBT  Source Categories: []  Category Map:[]|
|  |  qBT URL: []    Username: []    Password: [****]                 |
|  |  [Test Connection]                                               |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | NAMING TEMPLATES                                                 |
|  |  music:     [Artist.Album.Source.Codec-Group                    ]|
|  |  movies:    [Name.Year.Resolution.Source.Codec-Group            ]|
|  |  tv:        [Name.S##E##.Resolution.Source.Codec-Group          ]|
|  |  books:     [Title.Author.Year.Format-Group                     ]|
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | TORRENTLEECH PREFERENCES                                        |
|  |  Min Uploads/Month: [10]  Min Seed Copies: [10]  Min Seed Days: [7]|
|  |  Inactivity Warning (weeks): [3]  Absence Notice (weeks): [4]  |
|  |  [x] Enforce Activity Minimums                                  |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | PUSH NOTIFICATIONS (ntfy)                                       |
|  |  [x] Enable ntfy Notifications                                  |
|  |  ntfy Server URL: [https://ntfy.sh]                             |
|  |  ntfy Topic:      [torrup-alerts]                               |
|  +------------------------------------------------------------------+
|                                                                      |
|  [Save Settings]                                                    |
+---------------------------------------------------------------------+
```

### Sections

| Section | Fields |
|---------|--------|
| **General** | output_dir (with browse picker), release_group, exclude_dirs, theme |
| **Automation (Beta)** | test_mode, enable_auto_upload, auto_scan_interval |
| **Media Roots + Defaults** | Per-type: enabled, auto_scan, path (with browse picker), default_category |
| **Metadata Extraction** | extract_metadata, extract_thumbnails |
| **qBitTorrent Integration** | qbt_enabled, qbt_auto_add, qbt_tag, qbt_auto_source, qbt_source_categories, qbt_category_map, qbt_url, qbt_user, qbt_pass, test connection button |
| **Naming Templates** | Per-type: template pattern string |
| **TorrentLeech Preferences** | tl_min_uploads_per_month, tl_min_seed_copies, tl_min_seed_days, tl_inactivity_warning_weeks, tl_absence_notice_weeks, tl_enforce_activity |
| **Push Notifications (ntfy)** | ntfy_enabled, ntfy_url, ntfy_topic |

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Section Cards** | `.card .mb-6` | Grouped settings with section titles |
| **Section Titles** | `h2.section-title` | Card headers |
| **Text Inputs** | `.input` | Path, template, and value fields |
| **Dropdowns** | `.input` (select) | Category selectors, theme picker |
| **Checkboxes** | `.checkbox-field` | Enable/disable toggles |
| **Path Inputs** | `.path-input-group` | Input + Browse button for directory picking |
| **Directory Picker** | `.modal` | Modal dialog for browsing filesystem directories |
| **Save Button** | `.btn-primary .btn-md` | Save all settings |
| **Test Connection** | `.btn-secondary .btn-sm` | Test qBitTorrent connectivity |

### Data Sources

| Data | Source |
|------|--------|
| Current settings | Template variables from Flask (rendered server-side) |
| Save settings | `POST /api/settings` |
| Browse directories | `GET /api/browse-dirs?path=X` |
| Test qBT connection | `POST /api/settings/qbt/test` |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [API](api.md) - API endpoints and responses
- [Implementation](implementation.md) - File structure and build info
