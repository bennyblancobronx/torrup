# Torrup CLI Reference

Complete command-line interface documentation for Torrup (Torrent Upload Tool).

## Design Principles

1. **CLI-first**: All functionality available via CLI; GUI wraps CLI commands
2. **Composable**: Commands can be piped and scripted
3. **Predictable**: Consistent flags, exit codes, and output formats
4. **Safe defaults**: Destructive operations require confirmation

## Global Options

These options work with all commands:

| Flag | Description |
|------|-------------|
| `--help`, `-h` | Show help for command |
| `--version`, `-v` | Show version |
| `--json` | Output as JSON |
| `--quiet`, `-q` | Suppress non-essential output |
| `--verbose` | Verbose output for debugging |
| `--config PATH` | Use alternate config file |

## Exit Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | `EXIT_SUCCESS` | Command completed successfully |
| 1 | `EXIT_ERROR` | General error |
| 2 | `EXIT_INVALID_ARGS` | Invalid arguments or flags |
| 3 | `EXIT_NOT_FOUND` | Resource not found (item, file, setting) |
| 4 | `EXIT_DUPLICATE` | Duplicate detected on tracker |
| 5 | `EXIT_API_ERROR` | API or network error |
| 6 | `EXIT_MISSING_DEP` | Missing dependency (mediainfo/mktorrent) |

---

## Settings Commands

### torrup settings get

Display configuration settings.

```bash
# Get all settings
torrup settings get

# Get specific setting
torrup settings get <key>

# JSON output
torrup settings get --json
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `key` | No | Specific setting key to retrieve |

**Available Keys:**

| Key | Type | Description |
|-----|------|-------------|
| `browse_base` | string | Base path for media browsing |
| `output_dir` | string | Output directory for torrents/NFOs |
| `exclude_dirs` | string | Comma-separated folders to exclude |
| `templates` | object | Naming templates per media type |
| `qbt_enabled` | string | Enable qBitTorrent (1/0) |
| `qbt_url` | string | qBitTorrent WebUI URL |
| `qbt_user` | string | qBitTorrent username |
| `qbt_pass` | string | qBitTorrent password |
| `qbt_auto_add` | string | Auto-add to qBT after upload (1/0) |
| `qbt_auto_source` | string | Monitor qBT for completed downloads (1/0) |
| `qbt_tag` | string | Tag for Torrup-added torrents |
| `qbt_source_categories` | string | Categories to monitor (comma-separated) |
| `qbt_category_map` | string | Optional map of media_type to qBT category (CSV or JSON) |

**Examples:**

```bash
# Get all settings
torrup settings get

# Get specific setting
torrup settings get browse_base
# Output: /volume/media

# Get as JSON
torrup settings get --json
# Output: {"browse_base": "/volume/media", ...}
```

**Exit Codes:**
- 0: Success
- 3: Setting key not found

---

### torrup settings set

Update a configuration setting.

```bash
torrup settings set <key> <value>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `key` | Yes | Setting key to update |
| `value` | Yes | New value |

**Examples:**

```bash
# Set output directory
torrup settings set output_dir /app/output

# Set excluded directories
torrup settings set exclude_dirs "torrents,downloads,tmp,trash"

# Set naming template
torrup settings set templates.movies "Name.Year.Resolution.Source-Group"
```

**Exit Codes:**
- 0: Success
- 2: Invalid key or value
- 3: Setting key not found

---

## qBitTorrent Commands

### torrup qbt test

Test qBitTorrent connection.

```bash
torrup qbt test
```

**Exit Codes:**
- 0: Success
- 2: qBT disabled
- 5: API or connection error

---

### torrup qbt add

Add a torrent to qBitTorrent.

```bash
torrup qbt add --torrent /path/file.torrent --save-path /path/content --category movies
```

**Flags:**

| Flag | Required | Description |
|------|----------|-------------|
| `--torrent` | Yes | Path to `.torrent` file |
| `--save-path` | Yes | Path to the content data |
| `--category` | No | qBT category |

**Exit Codes:**
- 0: Success
- 2: Invalid args or qBT disabled
- 5: API or connection error

---

### torrup qbt monitor

Monitor qBitTorrent for completed downloads and add to queue.

```bash
# Run one scan and exit
torrup qbt monitor --once
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--once` | Run a single scan and exit |

**Exit Codes:**
- 0: Success
- 2: qBT auto-source disabled

---

## Browse Commands

### torrup browse

Browse media library by type.

```bash
torrup browse <media_type> [path]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `media_type` | Yes | One of: music, movies, tv, books |
| `path` | No | Subdirectory to browse (relative to media root) |

**Flags:**

| Flag | Description |
|------|-------------|
| `--depth N` | Max directory depth (default: 1) |
| `--show-files` | Include files in output |

**Output Fields:**

| Field | Description |
|-------|-------------|
| `name` | Directory or file name |
| `path` | Full path |
| `type` | `dir` or `file` |
| `size` | Size in bytes (files only) |
| `modified` | Last modified timestamp |

**Examples:**

```bash
# Browse music library
torrup browse music

# Browse specific movie year
torrup browse movies 2024

# Include files
torrup browse tv --show-files

# JSON output
torrup browse movies --json
```

**Exit Codes:**
- 0: Success
- 2: Invalid media type
- 3: Path not found

---

## Scan Commands

### torrup scan

Scan a media library directory for releases not yet on the tracker, and optionally queue them for upload. Currently supports music only.

```bash
torrup scan <media_type> <path> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `media_type` | Yes | One of: music, movies, tv, books (music only in current version) |
| `path` | Yes | Path to the library directory to scan |

**Flags:**

| Flag | Description |
|------|-------------|
| `--recursive`, `-r` | Recursive scan |
| `--dry-run` | Identify missing releases only; do not add to queue |

**Behavior (music):**

1. Iterates over artist directories, then album subdirectories
2. Extracts metadata from each album
3. Generates a release name and checks the tracker for duplicates
4. If not found on the tracker, queues the album for upload (unless `--dry-run`)
5. Calculates a certainty score; albums below 80% are queued as `pending_approval`
6. Includes a 1-second delay between checks for rate-limit protection

**Output:**

```
Scanning 42 artists in /volume/media/music...
Checking: Artist-Album-2024-FLAC-torrup... MISSING -> Queuing
Checking: Artist-Album-2023-FLAC-torrup... FOUND (Skipping)

Scan Complete.
Found on TL: 30
Missing:     12
Queued:      12
```

**Examples:**

```bash
# Scan music library and queue missing releases
torrup scan music /volume/media/music

# Dry run -- identify missing releases without queuing
torrup scan music /volume/media/music --dry-run
```

**Exit Codes:**
- 0: Success
- 1: Error (unsupported media type or scan failure)

---

## Queue Commands

### torrup queue add

Add item to upload queue.

```bash
torrup queue add <media_type> <path> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `media_type` | Yes | One of: music, movies, tv, books |
| `path` | Yes | Path to media item |

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--category N` | Per media type | Tracker category ID (e.g. TorrentLeech) |
| `--tags csv` | None | Comma-separated tags |
| `--release-name NAME` | Auto-generated | Override release name |

**Category Defaults (TorrentLeech example):**

| Media Type | Category ID | Label |
|------------|-------------|-------|
| music | 31 | Music :: Audio |
| movies | 14 | Movies :: BlurayRip |
| tv | 26 | TV :: Episodes (SD) |
| books | 45 | Books :: EBooks |

**Examples:**

```bash
# Add movie with defaults
torrup queue add movies "/volume/media/movies/Inception.2010.1080p.BluRay"

# Add with custom category and tags
torrup queue add music "/volume/media/music/Artist - Album" --category 31 --tags "FLAC,Lossless"

# Add with custom release name
torrup queue add tv "/volume/media/tv/Show.S01E01" --release-name "Show.S01E01.720p.HDTV-GROUP"
```

**Output:**

```
Added to queue: id=42, release_name=Inception.2010.1080p.BluRay-Torrup
```

**Exit Codes:**
- 0: Success
- 2: Invalid arguments
- 3: Path not found

---

### torrup queue list

List items in upload queue.

```bash
torrup queue list [options]
```

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--status STATUS` | All | Filter by status |
| `--media-type TYPE` | All | Filter by media type |
| `--limit N` | 50 | Max items to return |
| `--offset N` | 0 | Skip first N items |

**Status Values:**

| Status | Description |
|--------|-------------|
| `queued` | Waiting to be processed |
| `preparing` | Generating NFO/torrent |
| `uploading` | Uploading to tracker (e.g. TorrentLeech) |
| `success` | Upload completed |
| `failed` | Upload failed |
| `duplicate` | Duplicate detected |

**Output Fields:**

| Field | Description |
|-------|-------------|
| `id` | Queue item ID |
| `release_name` | Release name |
| `media_type` | Media type |
| `category` | Category ID |
| `status` | Current status |
| `created_at` | When added |
| `updated_at` | Last update |
| `message` | Status message or error |

**Examples:**

```bash
# List all
torrup queue list

# List queued items only
torrup queue list --status queued

# List failed items as JSON
torrup queue list --status failed --json

# Paginate
torrup queue list --limit 10 --offset 20
```

**Exit Codes:**
- 0: Success

---

### torrup queue update

Update a queue item.

```bash
torrup queue update <id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Queue item ID |

**Flags:**

| Flag | Description |
|------|-------------|
| `--release-name NAME` | Update release name |
| `--category N` | Update category |
| `--tags csv` | Update tags |
| `--status STATUS` | Update status |
| `--approval STATUS` | Set approval status: `approved`, `pending_approval`, or `rejected` |

**Examples:**

```bash
# Update release name
torrup queue update 42 --release-name "New.Release.Name-GROUP"

# Reset failed item to queued
torrup queue update 42 --status queued

# Update multiple fields
torrup queue update 42 --category 14 --tags "1080p,BluRay"
```

**Exit Codes:**
- 0: Success
- 2: Invalid arguments
- 3: Item not found

---

### torrup queue delete

Remove item from queue.

```bash
torrup queue delete <id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Queue item ID |

**Flags:**

| Flag | Description |
|------|-------------|
| `--force` | Skip confirmation |

**Examples:**

```bash
# Delete with confirmation
torrup queue delete 42

# Delete without confirmation
torrup queue delete 42 --force
```

**Exit Codes:**
- 0: Success
- 3: Item not found

---

### torrup queue run

Start background worker to process queue.

```bash
torrup queue run [options]
```

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--once` | False | Process one item and exit |
| `--interval N` | 30 | Seconds between queue checks |
| `--max-concurrent N` | 1 | Max concurrent uploads |

**Examples:**

```bash
# Run continuously
torrup queue run

# Process single item
torrup queue run --once

# Custom interval
torrup queue run --interval 60
```

**Exit Codes:**
- 0: Success (normal exit)
- 1: Error during processing
- 6: Missing dependency

---

## Prepare and Upload Commands

### torrup prepare

Generate NFO, torrent, and XML for a queue item without uploading.

```bash
torrup prepare <id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Queue item ID |

**Flags:**

| Flag | Description |
|------|-------------|
| `--force` | Regenerate even if files exist |
| `--output-dir PATH` | Override output directory |

**Generated Files:**

| File | Description |
|------|-------------|
| `<release_name>.nfo` | MediaInfo output |
| `<release_name>.torrent` | Torrent file (private, v1) |
| `<release_name>.xml` | XML metadata sidecar |

**Examples:**

```bash
# Prepare item
torrup prepare 42

# Force regenerate
torrup prepare 42 --force

# Custom output
torrup prepare 42 --output-dir /tmp/test
```

**Exit Codes:**
- 0: Success
- 3: Item not found
- 6: Missing mediainfo or mktorrent

---

### torrup upload

Upload a prepared queue item to tracker (e.g. TorrentLeech).

```bash
torrup upload <id> [options]
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Queue item ID |

**Flags:**

| Flag | Description |
|------|-------------|
| `--skip-dup-check` | Skip duplicate check |
| `--dry-run` | Validate without uploading |

**Examples:**

```bash
# Upload item
torrup upload 42

# Dry run
torrup upload 42 --dry-run

# Skip duplicate check
torrup upload 42 --skip-dup-check
```

**Exit Codes:**
- 0: Success
- 3: Item not found
- 4: Duplicate detected
- 5: API error

---

### torrup check-dup

Check if release exists on tracker (e.g. TorrentLeech).

```bash
torrup check-dup <release_name>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `release_name` | Yes | Release name to check |

**Output:**

```bash
# Not found
No duplicate found for: Release.Name.Here

# Found
Duplicate found: Release.Name.Here
  - Torrent ID: 123456
  - Uploaded: 2024-01-15
```

**Examples:**

```bash
# Check release
torrup check-dup "Inception.2010.1080p.BluRay.x264-GROUP"
```

**Exit Codes:**
- 0: No duplicate found
- 4: Duplicate found
- 5: API error

---

## Upload History Commands

### torrup uploads list

List upload history.

```bash
torrup uploads list [options]
```

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--status STATUS` | All | Filter by status |
| `--media-type TYPE` | All | Filter by media type |
| `--limit N` | 50 | Max items to return |
| `--since DATE` | None | Items since date (YYYY-MM-DD) |

**Examples:**

```bash
# List recent uploads
torrup uploads list --limit 10

# List successful uploads
torrup uploads list --status success

# JSON output
torrup uploads list --json
```

**Exit Codes:**
- 0: Success

---

### torrup uploads show

Show details of a specific upload.

```bash
torrup uploads show <id>
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Upload history ID |

**Output Fields:**

| Field | Description |
|-------|-------------|
| `id` | Upload ID |
| `torrent_id` | Tracker-specific torrent ID (e.g. TorrentLeech ID) |
| `release_name` | Release name |
| `media_type` | Media type |
| `category` | Category ID |
| `tags` | Tags used |
| `torrent_path` | Path to torrent file |
| `nfo_path` | Path to NFO file |
| `xml_path` | Path to XML file |
| `created_at` | Upload timestamp |
| `status` | Upload status |
| `message` | Status message |

**Examples:**

```bash
# Show upload details
torrup uploads show 42

# JSON output
torrup uploads show 42 --json
```

**Exit Codes:**
- 0: Success
- 3: Upload not found

---

## Activity Commands

### torrup activity

Show TorrentLeech activity health for the current month. Reports upload counts, projected pace, and whether the monthly minimum is at risk.

```bash
torrup activity
```

**Flags:**

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |

**Output Fields:**

| Field | Description |
|-------|-------------|
| `uploads` | Successful uploads this month |
| `queued` | Items currently queued |
| `projected` | Projected uploads by end of month at current pace |
| `minimum` | Monthly minimum upload target |
| `needed` | Remaining uploads needed to hit the minimum |
| `days_remaining` | Days left in the current month |
| `enforce` | Whether activity enforcement is enabled |
| `pace` | 7-day rolling average uploads per day (null if no data) |
| `critical` | True if projected uploads are below the monthly minimum |

**Output:**

```
Uploads this month: 14
Queued:             8
Projected:          22 / 20
Needed:             6
Days remaining:     15
Enforce:            yes
Pace (7d avg):      1.4/day
```

If projected uploads fall below the minimum, a warning is displayed:

```
WARNING: Projected uploads are below the monthly minimum.
```

**Examples:**

```bash
# Show activity health
torrup activity

# JSON output
torrup activity --json
```

**Exit Codes:**
- 0: Success

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TL_ANNOUNCE_KEY` | Tracker announce/passkey (e.g. TorrentLeech, required) |
| `TORRUP_DB_PATH` | Database path (default: ./torrup.db) |
| `TORRUP_OUTPUT_DIR` | Output directory override |
| `TORRUP_CONFIG` | Config file path |
| `TORRUP_LOG_LEVEL` | Log level: DEBUG, INFO, WARN, ERROR |
| `TORRUP_LOG_FORMAT` | Log format: text, json |

---

## Scripting Examples

### Batch Add from Directory

```bash
#!/bin/bash
for dir in /volume/media/movies/*/; do
    torrup queue add movies "$dir" --quiet
done
```

### Process and Report

```bash
#!/bin/bash
torrup queue run --once
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed"
    torrup queue list --status failed --json | jq '.[] | .release_name'
fi
```

### Check All for Duplicates

```bash
#!/bin/bash
torrup queue list --status queued --json | jq -r '.[].release_name' | while read name; do
    if torrup check-dup "$name" > /dev/null 2>&1; then
        echo "OK: $name"
    else
        echo "DUP: $name"
    fi
done
```

### Retry Failed Items

```bash
#!/bin/bash
torrup queue list --status failed --json | jq -r '.[].id' | while read id; do
    torrup queue update "$id" --status queued
done
torrup queue run
```

---

## Implementation Status

| Command | Status | Notes |
|---------|--------|-------|
| `torrup settings get` | Implemented | v0.1.1 |
| `torrup settings set` | Implemented | v0.1.1 |
| `torrup browse` | Implemented | v0.1.1 |
| `torrup queue add` | Implemented | v0.1.1 |
| `torrup queue list` | Implemented | v0.1.1 |
| `torrup queue update` | Implemented | v0.1.1 |
| `torrup queue delete` | Implemented | v0.1.1 |
| `torrup queue run` | Implemented | v0.1.1 |
| `torrup prepare` | Implemented | v0.1.1 |
| `torrup upload` | Implemented | v0.1.1 |
| `torrup check-dup` | Implemented | v0.1.1 |
| `torrup uploads list` | Implemented | v0.1.1 |
| `torrup uploads show` | Implemented | v0.1.1 |
| `torrup scan` | Implemented | v0.1.2 (music only) |
| `torrup qbt test` | Implemented | v0.1.4 |
| `torrup qbt add` | Implemented | v0.1.4 |
| `torrup qbt monitor` | Implemented | v0.1.4 |
| `torrup activity` | Implemented | v0.1.8 |
