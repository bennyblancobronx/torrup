# TorrentLeech Upload SME Guide

*Note: This document is a specific tracker integration guide for TorrentLeech. Torrup supports multiple trackers, but adheres to these rules when interacting with TorrentLeech.*

Complete reference for uploading TV Shows, Movies, Music, and Books to TorrentLeech.

**Source Documents:**
- `[RULES]` = Rules for uploaders (zdeev, Sep 2019, updated Feb 2020)
- `[CATEGORIES]` = Categories explained (zdeev, Mar 2018)
- `[FAQ]` = Frequently Asked Questions (zdeev, May 2018)
- `[GUIDE]` = Uploading Guide (zdeev, Feb 2020)
- `[API]` = API documentation (zdeev, Jan 2021, updated Feb 2025)

---

## Table of Contents

1. [General Rules](#general-rules)
2. [Naming Rules](#naming-rules)
3. [NFO Requirements](#nfo-requirements)
4. [Torrent File Creation](#torrent-file-creation)
5. [Category Reference](#category-reference)
6. [External Metadata](#external-metadata)
7. [TV Shows](#1-tv-shows)
8. [Movies](#2-movies)
9. [Music](#3-music)
10. [Books](#4-books)
11. [Upload API](#upload-api)
12. [Validation Checklist](#validation-checklist)
13. [Source Reference](#source-reference)

---

## General Rules

### Torrent Format

| Rule | Details | Source |
|------|---------|--------|
| Torrent version | **v1 only** - no Hybrid or v2 torrents | `[RULES]` General rules |
| Private flag | Must be set to private | `[GUIDE]` Step 2 |

### Seeding Requirements

| Rule | Details | Source |
|------|---------|--------|
| Minimum seeding | Until **10 copies exist** OR **1 week**, whichever comes first | `[RULES]` General rules |
| Delete window | 24 hours to self-delete; after that contact mod in #tluppers | `[RULES]` General rules |
| Don't delete | Content seeded to many users unless absolutely necessary | `[RULES]` General rules |

### Scene vs P2P Content

| Content Type | Rule | Source |
|--------------|------|--------|
| Scene Movies/TV | Can be unRARed (bot does this since early 2020) | `[RULES]` General rules |
| Scene Games/Apps | **Must stay in original RAR format** | `[RULES]` General rules |
| Scene Subs (Movies/TV) | **Must stay in original format** | `[RULES]` General rules |
| P2P content | Should be original form, but unRAR allowed | `[RULES]` General rules |

### Pack Rules

| Rule | Details | Source |
|------|---------|--------|
| Encouraged packs | TV Season packs only | `[RULES]` Pack rules |
| Season completeness | **ALL episodes** required - no mid-season packs | `[RULES]` Pack rules |
| Anime exception | Anime seasons may differ; mid-season allowed | `[RULES]` Pack rules |
| Other packs | Singles must be uploaded first | `[RULES]` Pack rules |
| 0-day packs | Excluded from singles-first rule (apps, FLAC, MP3, comics) | `[RULES]` Pack rules |
| Mixed quality | **NOT allowed** - all 4K, 1080p, or 720p | `[RULES]` Pack rules |
| Quality exception | Can mix if lower res unavailable (e.g., S01-S03 at 480p, S04+ at 1080p) | `[RULES]` Pack rules |
| Own packs | Use RAR in **'store' mode** | `[RULES]` General rules |

### Duplicate Rules

| Rule | Details | Source |
|------|---------|--------|
| No dupes for unRAR | Creating duplicates of existing releases just to unRAR is **not allowed** | `[RULES]` General rules |

### Banned Content

| Content | Rule | Source |
|---------|------|--------|
| BONE releases | **Not allowed** | `[RULES]` Additional content rules |
| YIFY releases | **Not allowed** | `[RULES]` Additional content rules |
| Retagged content | **Not allowed** - ask uploader first if unsure | `[RULES]` Additional content rules |
| Porn (any type) | **Not allowed** - includes japanese/manga games. Use pussytorrents.org | `[RULES]` General rules, `[CATEGORIES]` |
| Donations | **Never ask** in any form | `[RULES]` Additional content rules |

### Timed Releases

| Group | Rule | Source |
|-------|------|--------|
| Framestor | Wait for timer to expire | `[RULES]` Additional content rules |
| FLUX | Wait for timer to expire | `[RULES]` Additional content rules |
| BeyondHD | Wait for timer to expire | `[RULES]` Additional content rules |
| Note | If you don't know how to check timers, don't upload these | `[RULES]` Additional content rules |

### RARBG Content

| Rule | Details | Source |
|------|---------|--------|
| Allowed | Yes, with site tag | `[RULES]` Additional content rules |
| Required cleanup | Remove redundant files: `rarbg.txt`, `rarbg.exe`, etc. | `[RULES]` Additional content rules |

### Upscaled Content

| Rule | Details | Source |
|------|---------|--------|
| Naming | Must explicitly contain **"upscaled"** in the name | `[RULES]` Additional content rules |
| When allowed | Only when improving over existing HD content | `[RULES]` Additional content rules |

### Ads in Uploads

| Rule | Details | Source |
|------|---------|--------|
| General | **Never allowed** | `[RULES]` Ads in uploads |
| Screenshots | Links to screenshots that could be seen as ads - check with uploader if unsure | `[RULES]` Ads in uploads |
| CAM exception | CAMs allowed when no better source exists | `[RULES]` Ads in uploads |
| CAM deletion | If better source reported, CAM torrent will be deleted | `[RULES]` Ads in uploads |

### Encouraged Practices

| Practice | Source |
|----------|--------|
| Upload screenshots for TV/Movies | `[RULES]` General rules |
| Add tags to uploads | `[RULES]` General rules |

### Activity Requirements

| Requirement | Details | Source |
|-------------|---------|--------|
| Minimum uploads | **10 per month** expected | `[RULES]` Activity rules |
| Inactivity | PM warning after few weeks, then status revoked | `[RULES]` Activity rules |
| Extended absence | PM zdeev if away 4+ weeks | `[RULES]` Activity rules |
| Flexibility | If sources don't permit 10/month, PM to discuss | `[RULES]` Activity rules |

### Support Channels

| Channel | Purpose | Source |
|---------|---------|--------|
| IRC #tluppers | Uploader chat and questions | `[FAQ]` |
| PM zdeev on IRC | Get access to #tluppers | `[FAQ]` |
| Contact zdeev | Questions about rules | `[RULES]` |

---

## Naming Rules

**Source:** `[RULES]` Naming rules (Feb 2020 post)

### Universal Pattern

All names use **dots (`.`)** as separators. Never use spaces.

### Movie Format

```
Name.Year.Resolution.Source.Video.Codec.Audio.Codec-ReleaseGroup
```

**Example:** `Phantom.Thread.2017.2160p.UHD.BluRay.REMUX.HDR.HEVC.DTS-X-EPSiLON`

### TV Format

```
Name.S##E##.Resolution.Source.Audio.Codec.Video.Codec-ReleaseGroup
```

**Example:** `Heartless.S01.1080p.WEB-DL.DD5.1.x264-TrollHD`

### Audio Format

```
Artist.Name.Album.Name.Source.Audio.Codec-ReleaseGroup
```

**Example:** `Tool.Lateralus.CD.MP3-MARiBOR`

### Component Definitions

| Component | Definition | Source |
|-----------|------------|--------|
| Name | Title as shown on **IMDB or TVMaze** | `[RULES]` Naming rules |
| Year | Year shown on **IMDB or TVMaze** (exceptions possible) | `[RULES]` Naming rules |
| Resolution | Closest match (1800x1080 = 1080p) | `[RULES]` Naming rules |
| Source | Origin: Bluray, WEB-DL, etc. | `[RULES]` Naming rules |
| Video Codec | Encoding method - use MediaInfo if unsure | `[RULES]` Naming rules |
| Audio Codec | Audio encoding - use MediaInfo if unsure | `[RULES]` Naming rules |
| Release Group | Group name, or P2P/homerip. Can be omitted if not applicable | `[RULES]` Naming rules |

### Naming Consequences

| Issue | Result | Source |
|-------|--------|--------|
| Incorrect naming | Torrent may be **deleted** | `[RULES]` Naming rules |
| Minimum standard | Better than `ep1.mkv` or `song1.mp3` | `[RULES]` Naming rules |

---

## NFO Requirements

### NFO Requirement

| Rule | Details | Source |
|------|---------|--------|
| Required | **Every torrent** must have an NFO | `[RULES]` General rules |
| No scene NFO | Create one with **MediaInfo output** | `[RULES]` General rules |
| Anonymize | Remove personal info from MediaInfo | `[RULES]` General rules |
| Location | Does NOT need to be in file list - can be pasted into upload form | `[RULES]` General rules |

### Generating NFO

```bash
# Generate MediaInfo NFO
mediainfo "/path/to/video.mkv" > release_name.nfo

# Anonymize - remove file paths
mediainfo "/path/to/video.mkv" | grep -v "Complete name" > release_name.nfo
```

### HTML in NFOs

**Source:** `[FAQ]`

Allowed HTML tags in NFO text:

| Tag | Allowed Attributes |
|-----|-------------------|
| `<a>` | `href`, `target`, `name` |
| `<img>` | `src`, `alt` |
| `<span>` | `style` |
| `<b>`, `<strong>`, `<em>`, `<i>` | none |
| `<ul>`, `<li>`, `<ol>`, `<p>`, `<br>` | none |
| `avatar`, `center`, `font`, `colour` | n/a |

---

## Torrent File Creation

### Required Settings

| Setting | Value | Source |
|---------|-------|--------|
| Tracker URL | `https://tracker.torrentleech.org` | `[GUIDE]` Step 2 |
| Comment | Leave empty | `[GUIDE]` Step 2 |
| Private flag | **Yes** (tick the box) | `[GUIDE]` Step 2 |

### Source Tag

| Method | Details | Source |
|--------|---------|--------|
| mktorrent | Use `-s "TorrentLeech.org"` | `[FAQ]` |
| Without source tag | Must re-download .torrent from site after upload | `[FAQ]`, `[GUIDE]` Step 3 |
| Alternative | Use unique announce URL from upload page (no re-download needed) | `[GUIDE]` w00t comment |
| Exact format | `TorrentLeech.org` (case sensitive) | `[GUIDE]` HaArD comment Aug 2023 |

### Piece Size

**Source:** `[GUIDE]` HaArD comment, Beholder script

Target: **1500-2200 pieces** for optimal BitTorrent efficiency.

| Total Size | Piece Size | mktorrent `-l` flag |
|------------|------------|---------------------|
| < 50 MB | 32 KB | 15 |
| 50-150 MB | 64 KB | 16 |
| 150-350 MB | 128 KB | 17 |
| 350-512 MB | 256 KB | 18 |
| 512 MB - 1 GB | 512 KB | 19 |
| 1-2 GB | 1 MB | 20 |
| 2-4 GB | 2 MB | 21 |
| 4-8 GB | 4 MB | 22 |
| 8-16 GB | 8 MB | 23 |
| > 16 GB | 16 MB | 24 |

### mktorrent Command

```bash
mktorrent \
  -a "https://tracker.torrentleech.org" \
  -s "TorrentLeech.org" \
  -l 20 \
  -p \
  -o "Release.Name.torrent" \
  "/path/to/content"
```

| Flag | Purpose |
|------|---------|
| `-a` | Tracker announce URL |
| `-s` | Source tag (enables immediate seeding) |
| `-l` | Piece size as power of 2 |
| `-p` | Private torrent |
| `-o` | Output file |

### Seeding After Upload

**Source:** `[GUIDE]` Step 3

| Step | Details |
|------|---------|
| 1 | Re-download .torrent from site (unless using source tag) |
| 2 | Add torrent to client |
| 3 | Point **INTO** the directory where files are located |
| 4 | Skip hash check for large torrents (optional) |

---

## Category Reference

### Category Hierarchy

**Source:** `[CATEGORIES]`

When content fits multiple categories, use the **first match**:

```
1. Foreign (non-English primary audio)
2. Anime
3. Cartoons
4. Boxsets
5. Documentaries
6. 4K
7. Standard category (by source/quality)
```

### Complete Category Table

**Source:** `[CATEGORIES]`, `[API]` category table

#### TV Categories

| Category | Cat # | Description | Source |
|----------|-------|-------------|--------|
| Episodes | 26 | All SD single episodes | `[CATEGORIES]` |
| Episodes HD | 32 | 720p, 1080p, 2160p/4K single episodes | `[CATEGORIES]` |
| BoxSets | 27 | Season/Series packs (excludes anime/cartoons) | `[CATEGORIES]` |
| Foreign | 44 | Non-English primary audio (any quality) | `[CATEGORIES]` |

#### Movie Categories

| Category | Cat # | Description | Source |
|----------|-------|-------------|--------|
| Cam | 8 | CAM sourced encodes only | `[CATEGORIES]` |
| TS/TC | 9 | Telesyncs and Telecines only | `[CATEGORIES]` |
| HDRip | 43 | HDRip not from Bluray or Web | `[CATEGORIES]` |
| DVDRip/DVDScreener | 11 | Encodes from DVD source | `[CATEGORIES]` |
| DVD-R | 12 | Full/COMPLETE DVD image or DVD Remux | `[CATEGORIES]` |
| WEBRip | 37 | Encodes from streaming (iTunes, Netflix, Hulu, Amazon, etc.) | `[CATEGORIES]` |
| BlurayRip | 14 | Encodes from Bluray (H.264/H.265) | `[CATEGORIES]` |
| Bluray | 13 | Full/COMPLETE Bluray image or Bluray Remux | `[CATEGORIES]` |
| 4K | 47 | All 4K/2160p releases | `[CATEGORIES]` |
| Boxsets | 15 | Sequels, prequels, actor/director collections | `[CATEGORIES]` |
| Documentaries | 29 | All documentaries | `[CATEGORIES]` |
| Foreign | 36 | Non-English primary audio | `[CATEGORIES]` |

#### Music Categories

| Category | Cat # | Description | Source |
|----------|-------|-------------|--------|
| Audio | 31 | MP3, FLAC, OGG, all audio | `[CATEGORIES]` |
| Music Videos | 16 | Anything with moving pictures | `[CATEGORIES]` |

#### Book Categories

| Category | Cat # | Description | Source |
|----------|-------|-------------|--------|
| EBooks | 45 | All ebooks **including audiobooks** | `[CATEGORIES]` |
| Comics | 46 | All comics | `[CATEGORIES]` |

### Category Clarifications

**Source:** `[CATEGORIES]` comments (HaArD, Jun 2023)

#### Bluray vs BlurayRip

| Category | Content | Extensions |
|----------|---------|------------|
| Bluray (13) | Full disc OR **REMUX** | `.iso`, `.img`, folder structure, REMUX `.mkv` |
| BlurayRip (14) | Re-encoded from Bluray | `.mkv`, `.mp4`, `.avi` (H.264/H.265 encoded) |
| BDRip (in BlurayRip) | SD 576p/480p from Bluray | |

#### DVD Categories

| Category | Content | Source |
|----------|---------|--------|
| DVD-R (12) | Full disc image OR DVD Remux | `[CATEGORIES]` HaArD comment |
| DVDRip (11) | Encoded from DVD | `[CATEGORIES]` |

#### Special Cases

| Content | Category | Source |
|---------|----------|--------|
| HD-DVD encodes | Bluray (13) - treat as Bluray | `[CATEGORIES]` HaArD comment Oct 2021 |
| WEB-DL vs WEBRip | Both go in WEBRip (37) - same category | `[CATEGORIES]` Realuploads comment Jul 2023 |

---

## External Metadata

**Source:** `[API]`

### Summary by Category

| Category | External Source | API Parameter | Required? |
|----------|-----------------|---------------|-----------|
| Movies | IMDB | `imdb` | Optional but recommended |
| TV Shows | TVMaze | `tvmazeid` + `tvmazetype` | Optional but recommended |
| Music | None | - | N/A |
| Books | None | - | N/A |

**Note:** TorrentLeech uses **IMDB** (not TMDB) and **TVMaze** (not TVDB).

### IMDB (Movies)

| Detail | Value | Source |
|--------|-------|--------|
| Format | `tt` + 7-8 digits | `[API]` |
| Example | `tt1375666` (Inception) | `[API]` |
| Find it | URL: `https://www.imdb.com/title/tt1375666/` | - |

### TVMaze (TV Shows)

| Detail | Value | Source |
|--------|-------|--------|
| Format | Numeric ID (no prefix) | `[API]` |
| Example | `82` (Game of Thrones) | `[API]` |
| Find it | URL: `https://www.tvmaze.com/shows/82/game-of-thrones` | - |

### TVMaze Type Values

| Value | Meaning | Use For | Source |
|-------|---------|---------|--------|
| `1` | Series | Season packs, complete series | `[API]` |
| `2` | Episode | Single episodes | `[API]` |

---

## 1. TV Shows

### Category Selection

**Source:** `[CATEGORIES]`

```
Is primary audio NOT English?
  → YES → Category 44 (Foreign)
  → NO ↓

Is it a season pack or series collection?
  → YES → Category 27 (BoxSets)
  → NO ↓

Is resolution 720p or higher?
  → YES → Category 32 (Episodes HD)
  → NO → Category 26 (Episodes)
```

### Naming Examples

| Type | Example |
|------|---------|
| Single SD | `The.Office.S01E01.DVDRip.XviD-Group` |
| Single HD | `Breaking.Bad.S05E16.720p.BluRay.x264-DEMAND` |
| Single 1080p | `Stranger.Things.S04E09.1080p.WEB-DL.DDP5.1.x264-NTb` |
| Single 4K | `House.of.the.Dragon.S01E01.2160p.WEB-DL.DDP5.1.HDR.HEVC-Group` |
| Season Pack | `Severance.S01.1080p.ATVP.WEB-DL.DDP5.1.H.264-NTb` |
| Foreign | `Dark.S01.German.1080p.WEB-DL.DD5.1.x264-Group` |

### Season Pack Rules

| Rule | Details | Source |
|------|---------|--------|
| Completeness | **ALL episodes** required | `[RULES]` Pack rules |
| Mid-season | **Not allowed** | `[RULES]` Pack rules |
| Anime exception | Mid-season allowed for anime | `[RULES]` Pack rules |
| Mixed quality | **Not allowed** | `[RULES]` Pack rules |

### Folder Structure

```
Show.Name.S01.1080p.WEB-DL.DDP5.1.H.264-Group/
├── Show.Name.S01E01.1080p.WEB-DL.DDP5.1.H.264-Group.mkv
├── Show.Name.S01E02.1080p.WEB-DL.DDP5.1.H.264-Group.mkv
└── ... (all episodes)
```

### API Upload

```bash
# Single Episode
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=32' \
  -F 'tvmazeid=82' \
  -F 'tvmazetype=2' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload

# Season Pack
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=27' \
  -F 'tvmazeid=82' \
  -F 'tvmazetype=1' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload
```

---

## 2. Movies

### Category Selection

**Source:** `[CATEGORIES]`

```
Is primary audio NOT English?
  → YES → Category 36 (Foreign)
  → NO ↓

Is it a documentary?
  → YES → Category 29 (Documentaries)
  → NO ↓

Is it a multi-movie collection?
  → YES → Category 15 (Boxsets)
  → NO ↓

Is resolution 2160p/4K?
  → YES → Category 47 (4K)
  → NO ↓

What is the source?
  → CAM → Category 8
  → TS/TC → Category 9
  → HDRip → Category 43
  → DVDRip/DVDScreener → Category 11
  → DVD-R (full disc) → Category 12
  → WEBRip/WEB-DL → Category 37
  → BlurayRip (encoded) → Category 14
  → Bluray (full disc/REMUX) → Category 13
```

### Naming Examples

| Type | Example | Category |
|------|---------|----------|
| CAM | `Oppenheimer.2023.CAM.XviD-Group` | 8 |
| WEB-DL | `Dune.2021.1080p.WEB-DL.DDP5.1.Atmos.H.264-CMRG` | 37 |
| BlurayRip | `Interstellar.2014.1080p.BluRay.x264.DTS-FGT` | 14 |
| Bluray REMUX | `Avatar.2009.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-Group` | 13 |
| 4K | `Top.Gun.Maverick.2022.2160p.UHD.BluRay.REMUX.HDR.HEVC.Atmos-Group` | 47 |
| Foreign | `Parasite.2019.Korean.1080p.BluRay.x264-Group` | 36 |
| Documentary | `Free.Solo.2018.1080p.BluRay.x264-Group` | 29 |

### API Upload

```bash
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=14' \
  -F 'imdb=tt1375666' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload
```

---

## 3. Music

### Category Selection

**Source:** `[CATEGORIES]`

```
Does it contain video?
  → YES → Category 16 (Music Videos)
  → NO → Category 31 (Audio)
```

### Description

| Category | Description | Source |
|----------|-------------|--------|
| Audio (31) | Everything audio: MP3, FLAC, OGG, etc. | `[CATEGORIES]` |
| Music Videos (16) | Anything with moving pictures | `[CATEGORIES]` |

### Naming Examples

| Type | Example |
|------|---------|
| MP3 Album | `Tool.Lateralus.2001.CD.MP3-MARiBOR` |
| FLAC Album | `Pink.Floyd.The.Dark.Side.of.the.Moon.1973.CD.FLAC-Group` |
| WEB Release | `Taylor.Swift.Midnights.2022.WEB.FLAC-Group` |
| Discography | `The.Beatles.Discography.1963-1970.FLAC-Group` |
| Music Video | `Beyonce.Single.Ladies.2008.1080p.WEB-DL-Group` |

### Pack Rules

| Rule | Details | Source |
|------|---------|--------|
| 0-day packs | **Allowed** - FLAC, MP3 packs can be uploaded directly | `[RULES]` Pack rules |

### API Upload

```bash
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=31' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload
```

---

## 4. Books

### Category Selection

**Source:** `[CATEGORIES]`

```
Is it a comic/graphic novel?
  → YES → Category 46 (Comics)
  → NO → Category 45 (EBooks)
```

### Description

| Category | Description | Source |
|----------|-------------|--------|
| EBooks (45) | All ebooks **including audiobooks** | `[CATEGORIES]` |
| Comics (46) | All comics | `[CATEGORIES]` |

### Naming Examples

| Type | Example |
|------|---------|
| EPUB | `Stephen.King.The.Shining.1977.EPUB-Group` |
| PDF | `Richard.Feynman.Surely.Youre.Joking.1985.PDF-Group` |
| Audiobook | `Frank.Herbert.Dune.1965.AUDIOBOOK.MP3-Group` |
| Comic | `Marvel.Spider-Man.001.2022.CBR-Group` |

### Pack Rules

| Rule | Details | Source |
|------|---------|--------|
| 0-day packs | **Allowed** - comics packs can be uploaded directly | `[RULES]` Pack rules |

### API Upload

```bash
# EBook
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=45' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload

# Comic
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'category=46' \
  -F 'nfo=@release.nfo' \
  -F 'torrent=@release.torrent' \
  https://www.torrentleech.org/torrents/upload/apiupload
```

---

## Upload API

**Source:** `[API]`

### Access Requirements

| Requirement | Details | Source |
|-------------|---------|--------|
| Uploader status | Must be **full uploader** (not trial) | `[API]` |
| Trial uploaders | **Cannot use API** until promoted | `[API]` |

### Authentication

**Source:** `[API]` upload fields table (line 699)

TorrentLeech uses a **single key** for all API operations. This is your **Torrent Passkey** found in your profile.

| Term | Same Key | Location |
|------|----------|----------|
| `announcekey` (API parameter) | ✓ | Used in all API calls |
| Torrent Passkey | ✓ | TorrentLeech → Profile → "Torrent Passkey" |
| Announce URL key | ✓ | Embedded in personalized announce URLs |

**Important:** There is NO separate "API key". The 32-character Torrent Passkey serves all purposes:
1. API authentication (`announcekey` parameter)
2. Torrent announce URLs (tracker authentication)
3. Torrent downloads via API

### Endpoints

| Endpoint | URL | Method | Source |
|----------|-----|--------|--------|
| Upload | `https://www.torrentleech.org/torrents/upload/apiupload` | POST | `[API]` |
| Download | `https://www.torrentleech.org/torrents/upload/apidownload` | POST | `[API]` |
| Search | `https://www.torrentleech.org/api/torrentsearch` | POST | `[API]` |

### Upload Fields

| Field | Required | Type | Description | Source |
|-------|----------|------|-------------|--------|
| `announcekey` | **Yes** | string | Your 32-char announce key | `[API]` |
| `category` | **Yes** | integer | Category number | `[API]` |
| `nfo` | **Yes*** | file | NFO file upload | `[API]` |
| `description` | **Yes*** | string | Textual NFO (alternative to file) | `[API]` |
| `torrent` | **Yes** | file | .torrent file | `[API]` |
| `imdb` | No | string | IMDB ID (movies) | `[API]` |
| `tvmazeid` | No | integer | TVMaze ID (TV) | `[API]` |
| `tvmazetype` | No | integer | 1=series, 2=episode | `[API]` |
| `tags` | No | string | Comma-separated | `[API]` |

*Either `nfo` file OR `description` text required

### Torrup Implementation Status (Upload API)

**As of 2026-02-04**

| Field/Behavior | Implemented | Notes |
|----------------|-------------|-------|
| `announcekey` | Yes | Uses `TL_ANNOUNCE_KEY` env var. |
| `category` | Yes | Required. |
| `torrent` | Yes | Required. |
| `nfo` | Yes | Required by implementation. |
| `description` | No | Textual NFO not supported in current client. |
| `imdb` | No | Not sent. |
| `tvmazeid` | No | Not sent. |
| `tvmazetype` | No | Not sent. |
| `animeid` | No | Not sent. |
| `igdburl` | No | Not sent. |
| `tags` | Yes | Comma-separated tags supported. |

### Upload Response

| Response | Meaning | Source |
|----------|---------|--------|
| Numeric ID | Success - torrent ID | `[API]` reegun comment |
| Error text | Failure | `[API]` |

### Torrent Name

| Question | Answer | Source |
|----------|--------|--------|
| Where does name come from? | Copied from .torrent file name | `[API]` reegun comment Jan 2021 |

### Search API

**Source:** `[API]`

```bash
curl "https://www.torrentleech.org/api/torrentsearch" \
  -d "announcekey=YOUR_KEY" \
  -d "exact=1" \
  -d "query='Exact.Release.Name'"
```

| Field | Required | Description | Source |
|-------|----------|-------------|--------|
| `announcekey` | **Yes** | Your key | `[API]` |
| `query` | **Yes** | Search term in **single quotes** | `[API]` |
| `exact` | No | Set to `1` for exact match | `[API]` |

### Torrup Implementation Status (Search API)

**As of 2026-02-04**

| Behavior | Implemented | Notes |
|----------|-------------|-------|
| `announcekey` | Yes | Required. |
| `query` in single quotes | Yes | Always wraps with single quotes. |
| `exact` | Yes | Hardcoded to `1` (no fuzzy search). |

| Response | Meaning |
|----------|---------|
| `0` | Not found (safe to upload) |
| `1` | Found (duplicate exists) |

### Search API Known Issues

**Source:** `[API]` StarTech/zdeev comments Jan-Feb 2025

| Issue | Details |
|-------|---------|
| Partial matching | `exact=1` may still match partial names |
| Example | `Harlem.S03E05` matches `Godfather.of.Harlem.S03E05` |
| Status | Bug acknowledged, fixes attempted but may still occur |
| Workaround | Manual site search to verify before upload |

### Download API

```bash
curl -X POST \
  -F 'announcekey=YOUR_KEY' \
  -F 'torrentID=123456' \
  https://www.torrentleech.org/torrents/upload/apidownload \
  -o 'filename.torrent'
```

### Torrup Implementation Status (Download API)

**As of 2026-02-04**

Not implemented in Torrup.

---

## Validation Checklist

### Before Upload

- [ ] File(s) complete and not corrupted
- [ ] Not from banned groups (BONE, YIFY)
- [ ] Not retagged content
- [ ] If Framestor/FLUX/BeyondHD: timer expired
- [ ] If RARBG: redundant files removed
- [ ] If upscaled: "upscaled" in name

### Naming

- [ ] Uses dots as separators (no spaces)
- [ ] Name matches IMDB/TVMaze
- [ ] Year matches IMDB/TVMaze
- [ ] Resolution matches actual content
- [ ] Source accurately describes origin

### NFO

- [ ] NFO file exists
- [ ] Personal file paths removed
- [ ] MediaInfo included (for video)

### Torrent File

- [ ] Tracker: `https://tracker.torrentleech.org`
- [ ] Source tag: `TorrentLeech.org`
- [ ] Private flag: set
- [ ] Piece size: 1500-2200 pieces

### Category

- [ ] Hierarchy applied (Foreign > Boxsets > Docs > 4K > etc.)
- [ ] Correct category number selected

### Post-Upload

- [ ] API returned numeric torrent ID
- [ ] Torrent page loads
- [ ] Seeding started
- [ ] Seeding until 10 copies OR 1 week

---

## Error Reference

**Source:** `[FAQ]}

| Error | Meaning | Solution |
|-------|---------|----------|
| "Could not parse bencoded data" | Corrupted .torrent file | Re-download from tracker or recreate |
| Error 600 | Torrent doesn't exist | F5 to refresh (if just uploaded) or torrent was deleted |

---

## Quick Reference

### Category Numbers

```
TV:     26=SD  32=HD  27=BoxSets  44=Foreign
Movies: 8=Cam  9=TS  11=DVDRip  12=DVD-R  37=WEB  14=BDRip  13=BD  47=4K
        15=Boxsets  29=Docs  36=Foreign  43=HDRip
Music:  31=Audio  16=Videos
Books:  45=EBooks  46=Comics
```

### Naming Templates

```
TV Episode:  Show.Name.S01E01.1080p.WEB-DL.DDP5.1.x264-Group
TV Season:   Show.Name.S01.1080p.WEB-DL.DDP5.1.x264-Group
Movie:       Movie.Name.2023.1080p.BluRay.x264.DTS-Group
Music:       Artist.Album.2023.CD.FLAC-Group
Book:        Author.Title.2023.EPUB-Group
```

### mktorrent

```bash
mktorrent -a "https://tracker.torrentleech.org" -s "TorrentLeech.org" -l 20 -p -o "output.torrent" "/path"
```

---

## Source Reference

Every rule in this guide is sourced from official TorrentLeech documentation:

| Document | Author | Date | Topics |
|----------|--------|------|--------|
| Rules for uploaders | zdeev (Group Leader) | Sep 2019, Feb 2020 | General rules, naming, packs, banned content, activity |
| Categories explained | zdeev | Mar 2018 | Category definitions, hierarchy, Bluray vs BlurayRip |
| Frequently Asked Questions | zdeev | May 2018 | IRC, source tag, errors, HTML in NFOs |
| Uploading Guide | zdeev | Feb 2020 | Torrent creation, upload process, seeding |
| API documentation | zdeev | Jan 2021-Feb 2025 | Upload/download/search endpoints, fields, category numbers |

### Key Contributors (from comments)

| Person | Role | Contributions |
|--------|------|---------------|
| zdeev | Group Leader | All primary documentation |
| w00t | Super Administrator | Unique announce URL tip |
| reegun | Super Administrator | API response format clarification |
| HaArD | Moderator | Bluray/BlurayRip clarification, source tag format, piece size |
| Beholder | Uploader | Piece size calculation script |
| StarTech | Uploader | Search API bug reports |

### Contact

| For | Contact | Method |
|-----|---------|--------|
| Rules questions | zdeev | PM or #tluppers IRC |
| Category questions | #tluppers | IRC |
| API issues | zdeev | PM |
