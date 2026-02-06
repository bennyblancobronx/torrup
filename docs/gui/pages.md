# Torrup GUI Guide - Pages

Wireframes and component specifications for each page.

---

## Page 1: Dashboard

**Route:** `/`
**Template:** `index.html`
**Purpose:** Quick overview and most common actions

### Wireframe

```
+---------------------------------------------------------------------+
| DASHBOARD                                                            |
+---------------------------------------------------------------------+
|                                                                      |
|  +-------------+  +-------------+  +-------------+  +-----------+   |
|  |   QUEUED    |  |  UPLOADING  |  |   SUCCESS   |  |  FAILED   |   |
|  |     12      |  |      2      |  |     156     |  |    3      |   |
|  +-------------+  +-------------+  +-------------+  +-----------+   |
|                                                                      |
|  +------------------------------+  +----------------------------+   |
|  | QUICK ACTIONS                |  | RECENT ACTIVITY            |   |
|  |                              |  |                            |   |
|  |  [Browse Music]              |  |  Movie.Name.2024... OK     |   |
|  |  [Browse Movies]             |  |  Album.Name.FLAC... OK     |   |
|  |  [Browse TV]                 |  |  Show.S01E01... uploading  |   |
|  |  [Browse Books]              |  |  Release.Name... failed    |   |
|  |                              |  |                            |   |
|  |  [View Queue]                |  |  [View All]                |   |
|  +------------------------------+  +----------------------------+   |
|                                                                      |
|  +------------------------------------------------------------------+
|  | SYSTEM STATUS                                                    |
|  |                                                                  |
|  |  Worker: Running    |  mediainfo: OK  |  mktorrent: OK          |
|  |  Database: OK       |  API Key: Configured                      |
|  +------------------------------------------------------------------+
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Stat Cards** | `.card` | 4 cards with counts: Queued, Uploading, Success, Failed |
| **Quick Actions** | `.btn-secondary` | Buttons linking to browse page with type preselected |
| **Recent Activity** | `.table` | Last 5 queue items with status badges |
| **System Status** | `.card` | Worker state, dependency checks, API key status |

### Data Requirements

| Data | Source |
|------|--------|
| Queue counts | `GET /api/stats` |
| Recent items | `GET /api/queue?limit=5` |
| System status | `GET /api/system` |

---

## Page 2: Browse

**Route:** `/browse`
**Template:** `browse.html`
**Purpose:** Navigate media library and select items to queue

### Wireframe

```
+---------------------------------------------------------------------+
| BROWSE LIBRARY                                                       |
+---------------------------------------------------------------------+
|                                                                      |
|  Media Type: [Music v]    [Refresh]                                 |
|                                                                      |
|  Path: /music  >  Artist Name  >  Album Name                        |
|        [Home]     [Up One Level]                                    |
|                                                                      |
|  +------------------------------------------------------------------+
|  | [ ]  NAME                                              SIZE      |
|  +------------------------------------------------------------------+
|  | [ ]  [D] Subfolder A                                   --        |
|  | [ ]  [D] Subfolder B                                   --        |
|  | [x]  [D] Album.Name.2024.FLAC                          1.2 GB    |
|  | [x]  [D] Another.Album.2023.MP3                        450 MB    |
|  | [ ]  [F] cover.jpg                                     2.1 MB    |
|  +------------------------------------------------------------------+
|                                                                      |
|  Selected: 2 items (1.65 GB)                                        |
|                                                                      |
|  [Add to Queue]                                                     |
|                                                                      |
|  Tip: Select folders to upload. Click folder name to enter.        |
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Media Type Dropdown** | `.input` (select) | music, movies, tv, books |
| **Breadcrumb** | `.text-sm` | Current path with clickable segments |
| **Navigation Buttons** | `.btn-ghost` | Home (root) and Up (parent directory) |
| **File List** | `.table` | Checkbox, type icon, name (clickable), size |
| **Selection Summary** | `.text-secondary` | Count and total size of selected items |
| **Add to Queue** | `.btn-primary` | Primary action button |
| **Tips** | `.text-muted` | Help text for beginners |

### Interactions

| Action | Result |
|--------|--------|
| Click folder name | Navigate into folder |
| Click checkbox | Toggle selection |
| Change media type | Reset to root of that media type |
| Click Home | Return to media root |
| Click Up | Go to parent directory |
| Click Add to Queue | Add selected items, redirect to Queue page |

### Data Requirements

| Data | Source |
|------|--------|
| Directory listing | `GET /api/browse?media_type=X&path=Y` |

---

## Page 3: Queue

**Route:** `/queue`
**Template:** `queue.html`
**Purpose:** Manage pending and active uploads

### Wireframe

```
+---------------------------------------------------------------------+
| UPLOAD QUEUE                                                         |
+---------------------------------------------------------------------+
|                                                                      |
|  Filter: [All v]  [Queued] [Uploading] [Failed]    [Refresh]        |
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
|  |                                                                  |
|  |  [Save Changes]  [Cancel]                                       |
|  +------------------------------------------------------------------+
|                                                                      |
|  Tip: Edit release name, category, and tags before upload.         |
+---------------------------------------------------------------------+
```

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Filter Tabs** | `.btn-ghost` | All, Queued, Uploading, Failed quick filters |
| **Filter Dropdown** | `.input` (select) | Full status filter |
| **Queue Table** | `.table` | ID, type, release name, category, status, actions |
| **Action Buttons** | `.btn-ghost` `.btn-sm` | Edit, Delete, Retry, View |
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

### Action Icons

| Icon | Meaning |
|------|---------|
| E | Edit |
| X | Delete |
| R | Retry |
| V | View |

### Data Requirements

| Data | Source |
|------|--------|
| Queue list | `GET /api/queue` |
| Update item | `POST /api/queue/update` |
| Delete item | `POST /api/queue/delete` |

---

## Page 4: History

**Route:** `/history`
**Template:** `history.html`
**Purpose:** View past uploads and activity logs

### Wireframe

```
+---------------------------------------------------------------------+
| UPLOAD HISTORY                                                       |
+---------------------------------------------------------------------+
|                                                                      |
|  Tabs: [Uploads] [Activity]                                         |
|                                                                      |
|  Filter: [All v]  Date: [Last 7 days v]  Type: [All v]              |
|                                                                      |
|  +------------------------------------------------------------------+
|  | DATE       | RELEASE NAME               | STATUS | TRACKER ID    |
|  +------------------------------------------------------------------+
|  | 2026-02-03 | Movie.Name.2024.1080p...   | OK     | #1234567     |
|  | 2026-02-03 | Album.FLAC.2024...         | OK     | #1234566     |
|  | 2026-02-02 | Show.S01E01...             | DUP    | --           |
|  | 2026-02-02 | Book.Title...              | OK     | #1234565     |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | DETAILS: Movie.Name.2024.1080p.BluRay.x264-GROUP                 |
|  |                                                                  |
|  |  Tracker ID:        #1234567 (e.g. TorrentLeech)                 |
|  |  Category:         Movies :: BlurayRip                          |
|  |  Tags:             1080p, BluRay                                |
|  |  Uploaded:         2026-02-03 14:32:15                          |
|  |                                                                  |
|  |  Files Generated:                                               |
|  |    OK  Movie.Name.2024.1080p.BluRay.x264-GROUP.torrent         |
|  |    OK  Movie.Name.2024.1080p.BluRay.x264-GROUP.nfo             |
|  |    OK  Movie.Name.2024.1080p.BluRay.x264-GROUP.xml             |
|  +------------------------------------------------------------------+
+---------------------------------------------------------------------+
```

### Tabs

| Tab | Content |
|-----|---------|
| **Uploads** | Completed uploads with tracker IDs |
| **Activity** | Timestamped log of all actions (add, edit, delete, upload) |

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Tab Switcher** | `.btn-ghost` | Toggle between Uploads and Activity views |
| **Filters** | `.input` (select) | Status, date range, media type |
| **History Table** | `.table` | Date, release name, status, Tracker ID |
| **Details Panel** | `.card` | Click row to show full details |

### Data Requirements

| Data | Source |
|------|--------|
| Upload history | `GET /api/history` |
| Activity log | `GET /api/activity` |

---

## Page 5: Settings

**Route:** `/settings`
**Template:** `settings.html`
**Purpose:** Configure all application settings

### Wireframe

```
+---------------------------------------------------------------------+
| SETTINGS                                                             |
+---------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | GENERAL                                                          |
|  |                                                                  |
|  |  Output Directory:    [/app/output                              ]|
|  |  Excluded Folders:    [torrents,downloads,tmp,trash             ]|
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | MEDIA LIBRARIES                                                  |
|  |                                                                  |
|  |  TYPE      | ENABLED | PATH                    | CATEGORY       |
|  |  ----------|---------|-------------------------|----------------|
|  |  music     | [x]     | [/media/music          ]| [Audio v]      |
|  |  movies    | [x]     | [/media/movies         ]| [BluRay v]     |
|  |  tv        | [x]     | [/media/tv             ]| [Epis. v]      |
|  |  books     | [ ]     | [/media/books          ]| [EBooks v]     |
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | NAMING TEMPLATES                                                 |
|  |                                                                  |
|  |  music:     [Artist.Album.Source.Codec-Group                    ]|
|  |  movies:    [Name.Year.Resolution.Source.Codec-Group            ]|
|  |  tv:        [Name.S##E##.Resolution.Source.Codec-Group          ]|
|  |  books:     [Title.Author.Year.Format-Group                     ]|
|  +------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+
|  | SYSTEM                                                           |
|  |                                                                  |
|  |  Worker Status:   Running [Stop Worker]                         |
|  |  API Key:         Configured (via TL_ANNOUNCE_KEY env)          |
|  |  Dependencies:    mediainfo OK   mktorrent OK                   |
|  |  Database:        /app/torrup.db (156 KB)                       |
|  +------------------------------------------------------------------+
|                                                                      |
|  [Save All Settings]                                                |
|                                                                      |
+---------------------------------------------------------------------+
```

### Sections

| Section | Fields |
|---------|--------|
| **General** | output_dir, exclude_dirs |
| **Media Libraries** | Per-type: enabled (checkbox), path, default_category |
| **Naming Templates** | Per-type: template pattern string |
| **System** | Worker control, API key status, dependencies, database info |

### Components

| Component | Crisp Class | Description |
|-----------|-------------|-------------|
| **Section Cards** | `.card` | Grouped settings |
| **Section Titles** | `h3` (20px, weight 500) | Card headers |
| **Text Inputs** | `.input` | Path, template fields |
| **Dropdowns** | `.input` (select) | Category selectors |
| **Checkboxes** | `.checkbox` | Enable/disable toggles |
| **Save Button** | `.btn-primary` | Save all settings |
| **Stop/Start** | `.btn-secondary` | Worker control |

### Data Requirements

| Data | Source |
|------|--------|
| Current settings | Template variables from Flask |
| Save settings | `POST /api/settings` |
| System status | `GET /api/system` |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [API](api.md) - API endpoints and responses
- [Implementation](implementation.md) - Phases and file structure
