"""Background worker for automated media scanning and queuing."""

from __future__ import annotations

import time
from pathlib import Path

from src.api import check_exists
from src.db import db, get_media_roots, get_setting, get_excludes
from src.logger import logger
from src.utils import extract_metadata, is_excluded, now_iso, suggest_release_name


def auto_scan_worker() -> None:
    """Periodically scans enabled media roots for new content and queues them if missing on TL."""
    logger.info("Auto-scan worker started")
    
    while True:
        try:
            with db() as conn:
                enabled = get_setting(conn, "enable_auto_upload") == "1"
                interval_mins = int(get_setting(conn, "auto_scan_interval") or 60)
                excludes = get_excludes(conn)
                
                if not enabled:
                    time.sleep(60)
                    continue

                roots = get_media_roots(conn)
                for root in roots:
                    if not root["auto_scan"]:
                        continue
                    
                    # Check if it's time to scan this root
                    last_scan = root["last_scan"]
                    if last_scan:
                        # Simple check: has interval passed?
                        pass # For now we just scan every loop if auto_scan is on
                    
                    logger.info(f"Auto-scanning {root['media_type']} root: {root['path']}")
                    _scan_root(conn, root, excludes)
                    
                    # Update last scan time
                    conn.execute(
                        "UPDATE media_roots SET last_scan = ? WHERE media_type = ?",
                        (now_iso(), root["media_type"])
                    )
            
            # Wait for next interval
            time.sleep(interval_mins * 60)
            
        except Exception as e:
            logger.error(f"Auto-scan worker error: {e}", exc_info=True)
            time.sleep(300) # Sleep 5 mins on error


def _scan_root(conn, root, excludes):
    """Scan a specific root directory."""
    base_path = Path(root["path"])
    if not base_path.exists():
        return

    media_type = root["media_type"]
    category = root["default_category"]
    
    # Iterate over immediate children (folders/files as releases)
    for entry in base_path.iterdir():
        if is_excluded(entry, excludes):
            continue
        
        # Check if already in queue or history
        exists_in_db = conn.execute(
            "SELECT 1 FROM queue WHERE path = ?", (str(entry),)
        ).fetchone()
        
        if exists_in_db:
            continue

        metadata = extract_metadata(entry, media_type)
        release_name = _determine_release_name(entry, media_type, metadata)
        if not release_name:
            continue

        # Check TL
        if check_exists(release_name):
            logger.info(f"Auto-scan: {release_name} already on TL, skipping.")
            # Record it so we don't check again
            _add_to_queue_silent(conn, media_type, entry, release_name, category, "duplicate", "Found during auto-scan", metadata)
            continue

        # Not on TL, add to queue
        logger.info(f"Auto-scan: Found new content {release_name}, adding to queue.")
        _add_to_queue(conn, media_type, entry, release_name, category, metadata)


def _determine_release_name(path: Path, media_type: str, meta: dict) -> str:
    """Determine the release name, preferring tags for music."""
    if media_type == "music":
        if meta.get("artist") and meta.get("album"):
            # Format: Artist.Album.Year.Source.Audio.Codec-ReleaseGroup
            year = meta.get("year", "")
            name = f"{meta['artist']}.{meta['album']}"
            if year:
                name += f".{year}"
            
            # Add extension-based format if it's a file
            if path.is_file():
                ext = path.suffix.upper().replace(".", "")
                name += f".{ext}"
            else:
                # Check for FLAC/MP3 in children if folder
                first_file = next(path.rglob("*.*"), None)
                if first_file:
                    ext = first_file.suffix.upper().replace(".", "")
                    name += f".{ext}"
            
            from src.utils import sanitize_release_name
            return sanitize_release_name(name)
            
    return suggest_release_name(media_type, path)


def _add_to_queue(conn, media_type, path, release_name, category, metadata):
    """Add item to queue for processing."""
    conn.execute(
        """
        INSERT INTO queue (media_type, path, release_name, category, imdb, tvmazeid, tvmazetype, created_at, updated_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'queued')
        """,
        (
            media_type, 
            str(path), 
            release_name, 
            category, 
            metadata.get("imdb"), 
            metadata.get("tvmazeid"), 
            metadata.get("tvmazetype"), 
            now_iso(), 
            now_iso()
        )
    )


def _add_to_queue_silent(conn, media_type, path, release_name, category, status, message, metadata):
    """Add item to queue with a specific status (e.g. duplicate) to avoid re-scanning."""
    conn.execute(
        """
        INSERT INTO queue (media_type, path, release_name, category, imdb, tvmazeid, tvmazetype, created_at, updated_at, status, message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            media_type, 
            str(path), 
            release_name, 
            category, 
            metadata.get("imdb"), 
            metadata.get("tvmazeid"), 
            metadata.get("tvmazetype"), 
            now_iso(), 
            now_iso(), 
            status, 
            message
        )
    )
