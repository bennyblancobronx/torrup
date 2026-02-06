"""Scan CLI command."""

from __future__ import annotations

import time
from pathlib import Path

from src.api import check_exists
from src.config import CATEGORY_OPTIONS, MEDIA_TYPES
from src.db import db, get_setting
from src.utils import generate_release_name, now_iso, sanitize_release_name
from src.utils.metadata import extract_metadata
from src.cli.queue import calculate_certainty

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

def cmd_scan(cli) -> int:
    """Handle: torrup scan <media_type> <path>."""
    media_type = cli.args.media_type
    path_str = cli.args.path
    recursive = getattr(cli.args, "recursive", False)
    dry_run = getattr(cli.args, "dry_run", False)

    root_path = Path(path_str)
    if not root_path.exists():
        return cli.error(f"Path not found: {root_path}")

    # For music, we scan Artists -> Albums
    if media_type == "music":
        return _scan_music(cli, root_path, dry_run)
    
    return cli.error("Only music scanning is currently supported in this version.")


def _scan_music(cli, artists_dir: Path, dry_run: bool) -> int:
    """Scan music library for missing releases."""
    
    with db() as conn:
        release_group = get_setting(conn, "release_group") or "Torrup"
        default_cat = CATEGORY_OPTIONS["music"][0]["id"] # Audio

    count_found = 0
    count_missing = 0
    count_queued = 0

    artists = [d for d in artists_dir.iterdir() if d.is_dir()]
    print(f"Scanning {len(artists)} artists in {artists_dir}...")

    for artist_dir in sorted(artists):
        albums = [d for d in artist_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        
        for album_dir in albums:
            # 1. Extract Metadata
            try:
                meta = extract_metadata(album_dir, "music")
            except Exception:
                meta = {}
            
            # 2. Generate Release Name
            release_name = generate_release_name(meta, "music", release_group)
            
            if release_name == "unnamed" or "Unknown" in release_name:
                # Fallback to folder name
                release_name = sanitize_release_name(album_dir.name)

            print(f"Checking: {release_name}...", end="", flush=True)

            # 3. Check TL
            try:
                # Check exact generated name
                exists = check_exists(release_name, exact=False)
                if not exists:
                    # Check Artist Album fallback
                    fallback = sanitize_release_name(f"{artist_dir.name} {album_dir.name}")
                    exists = check_exists(fallback, exact=False)

                if exists:
                    print(" FOUND (Skipping)")
                    count_found += 1
                else:
                    print(" MISSING -> Queuing")
                    count_missing += 1
                    
                    if not dry_run:
                        # Queue it
                        certainty = calculate_certainty(meta, "music")
                        approval = "approved" if certainty >= 80 else "pending_approval"
                        
                        with db() as conn:
                            # Check if already queued
                            existing = conn.execute(
                                "SELECT id FROM queue WHERE path = ? AND status != 'failed'", 
                                (str(album_dir),)
                            ).fetchone()
                            
                            if not existing:
                                conn.execute(
                                    """
                                    INSERT INTO queue (
                                        media_type, path, release_name, category, tags, 
                                        status, created_at, updated_at, certainty_score, approval_status
                                    )
                                    VALUES (?, ?, ?, ?, ?, 'queued', ?, ?, ?, ?)
                                    """,
                                    ("music", str(album_dir), release_name, default_cat, "", 
                                     now_iso(), now_iso(), certainty, approval)
                                )
                                conn.commit()
                                count_queued += 1
            except Exception as e:
                print(f" Error: {e}")
            
            time.sleep(1.0) # Rate limit protection

    print("\nScan Complete.")
    print(f"Found on TL: {count_found}")
    print(f"Missing:     {count_missing}")
    print(f"Queued:      {count_queued}")
    
    return EXIT_SUCCESS
