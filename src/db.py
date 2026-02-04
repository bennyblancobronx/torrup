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
)


@contextmanager
def db():
    """Database connection context manager with thread safety."""
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
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
                default_category INTEGER NOT NULL DEFAULT 31
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
                status TEXT NOT NULL DEFAULT 'queued',
                message TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                torrent_path TEXT,
                nfo_path TEXT,
                xml_path TEXT,
                thumb_path TEXT
            )
            """
        )

        # Add thumb_path column if it doesn't exist (migration for existing DBs)
        try:
            conn.execute("ALTER TABLE queue ADD COLUMN thumb_path TEXT")
        except Exception:
            pass  # Column already exists

        # Defaults
        _ensure_setting(conn, "browse_base", "/volume/media")
        _ensure_setting(conn, "output_dir", str(DEFAULT_OUTPUT_DIR))
        _ensure_setting(conn, "exclude_dirs", DEFAULT_EXCLUDES)

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
        "INSERT INTO settings (key, value) VALUES (?, ?)"
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
