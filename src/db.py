"""Database helpers for SQLite operations."""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path

# Reentrant thread lock for SQLite operations (allows nested db() calls)
_db_lock = threading.RLock()

from src.config import (
    CATEGORY_OPTIONS,
    DB_PATH,
    DEFAULT_EXCLUDES,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_RELEASE_GROUP,
    DEFAULT_TEMPLATES,
    MEDIA_TYPES,
    QBT_DEFAULT_PASS,
    QBT_DEFAULT_URL,
    QBT_DEFAULT_USER,
)


@contextmanager
def db():
    """Database connection context manager with thread safety."""
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def init_db() -> None:
    """Initialize database schema and defaults."""
    with db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS media_roots (
                media_type TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                default_category INTEGER NOT NULL DEFAULT 31,
                auto_scan INTEGER NOT NULL DEFAULT 0,
                last_scan TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_type TEXT NOT NULL,
                path TEXT NOT NULL,
                release_name TEXT NOT NULL,
                category INTEGER NOT NULL,
                tags TEXT NOT NULL DEFAULT '',
                imdb TEXT,
                tvmazeid TEXT,
                tvmazetype TEXT,
                status TEXT NOT NULL DEFAULT 'queued',
                message TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                torrent_path TEXT,
                nfo_path TEXT,
                xml_path TEXT,
                thumb_path TEXT,
                certainty_score INTEGER DEFAULT 100,
                approval_status TEXT DEFAULT 'approved'
            )
            """
        )

        # Migration for existing DBs
        migrations = [
            "ALTER TABLE media_roots ADD COLUMN auto_scan INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE media_roots ADD COLUMN last_scan TEXT",
            "ALTER TABLE queue ADD COLUMN thumb_path TEXT",
            "ALTER TABLE queue ADD COLUMN imdb TEXT",
            "ALTER TABLE queue ADD COLUMN tvmazeid TEXT",
            "ALTER TABLE queue ADD COLUMN tvmazetype TEXT",
            "ALTER TABLE queue ADD COLUMN certainty_score INTEGER DEFAULT 100",
            "ALTER TABLE queue ADD COLUMN approval_status TEXT DEFAULT 'approved'",
        ]
        
        for migration in migrations:
            try:
                conn.execute(migration)
            except sqlite3.OperationalError:
                pass  # Already exists

        # Defaults
        _ensure_setting(conn, "browse_base", "/volume/media")
        _ensure_setting(conn, "output_dir", str(DEFAULT_OUTPUT_DIR))
        _ensure_setting(conn, "exclude_dirs", DEFAULT_EXCLUDES)
        _ensure_setting(conn, "auto_scan_interval", "60")  # Minutes
        _ensure_setting(conn, "enable_auto_upload", "0")  # Safety first

        for media_type in MEDIA_TYPES:
            base = get_setting(conn, "browse_base")
            default_path = str(Path(base) / media_type)
            default_category = CATEGORY_OPTIONS[media_type][0]["id"]
            conn.execute(
                """
                INSERT OR IGNORE INTO media_roots (media_type, path, enabled, default_category)
                VALUES (?, ?, 1, ?)
                """,
                (media_type, default_path, default_category),
            )

        for k, v in DEFAULT_TEMPLATES.items():
            _ensure_setting(conn, f"template_{k}", v)

        _ensure_setting(conn, "release_group", DEFAULT_RELEASE_GROUP)
        _ensure_setting(conn, "extract_metadata", "1")
        _ensure_setting(conn, "extract_thumbnails", "1")

        # qBitTorrent Settings
        _ensure_setting(conn, "qbt_enabled", "0")
        _ensure_setting(conn, "qbt_url", QBT_DEFAULT_URL)
        _ensure_setting(conn, "qbt_user", QBT_DEFAULT_USER)
        _ensure_setting(conn, "qbt_pass", QBT_DEFAULT_PASS)
        _ensure_setting(conn, "qbt_auto_add", "0")  # Auto add to qBT after upload
        _ensure_setting(conn, "qbt_tag", "Torrup")  # Tag for items added by Torrup
        _ensure_setting(conn, "qbt_auto_source", "0")  # Monitor qBT for completed downloads to upload
        _ensure_setting(conn, "qbt_source_categories", "music,movies,tv") # Categories to monitor in qBT

        conn.commit()


def _ensure_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Insert setting if it doesn't exist."""
    conn.execute(
        "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
        (key, value),
    )


def get_setting(conn: sqlite3.Connection, key: str) -> str:
    """Get a setting value by key."""
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else ""


def set_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Set a setting value."""
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def get_output_dir(conn: sqlite3.Connection | None = None) -> Path:
    """Get the configured output directory."""
    if conn is None:
        with db() as conn:
            path = get_setting(conn, "output_dir")
    else:
        path = get_setting(conn, "output_dir")
    out = Path(path) if path else DEFAULT_OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    return out


def get_media_roots(conn: sqlite3.Connection) -> list[dict]:
    """Get all media root configurations."""
    rows = conn.execute("SELECT * FROM media_roots").fetchall()
    return [dict(r) for r in rows]


def get_excludes(conn: sqlite3.Connection) -> list[str]:
    """Get list of excluded directory names."""
    excludes = get_setting(conn, "exclude_dirs")
    return [e.strip() for e in excludes.split(",") if e.strip()]
