"""qBitTorrent CLI commands."""

from __future__ import annotations

from pathlib import Path

from src.db import db, get_setting
from src.utils.qbittorrent import add_to_qbt, get_qbt_client

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INVALID_ARGS = 2
EXIT_API_ERROR = 5


def _qbt_enabled(conn) -> bool:
    return get_setting(conn, "qbt_enabled") == "1"


def cmd_qbt_test(cli) -> int:
    """Handle: torrup qbt test."""
    with db() as conn:
        if not _qbt_enabled(conn):
            return cli.error("qBT is disabled (qbt_enabled=0).", EXIT_INVALID_ARGS)

    client = get_qbt_client()
    if not client:
        return cli.error("Failed to connect to qBT. Check URL/user/pass.", EXIT_API_ERROR)

    try:
        version = client.app.version
    except Exception:
        version = "unknown"

    cli.output({"success": True, "version": version}, f"Connected. qBT version: {version}")
    return EXIT_SUCCESS


def cmd_qbt_add(cli) -> int:
    """Handle: torrup qbt add --torrent <path> --save-path <path>."""
    torrent_path = Path(cli.args.torrent)
    save_path = Path(cli.args.save_path)
    category = getattr(cli.args, "category", None)

    if not torrent_path.exists():
        return cli.error(f"Torrent file not found: {torrent_path}", EXIT_INVALID_ARGS)
    if not save_path.exists():
        return cli.error(f"Save path not found: {save_path}", EXIT_INVALID_ARGS)

    with db() as conn:
        if not _qbt_enabled(conn):
            return cli.error("qBT is disabled (qbt_enabled=0).", EXIT_INVALID_ARGS)

    ok = add_to_qbt(torrent_path, save_path, category=category)
    if not ok:
        return cli.error("Failed to add torrent to qBT.", EXIT_API_ERROR)

    cli.output({"success": True, "torrent": str(torrent_path)}, "Added to qBT.")
    return EXIT_SUCCESS


def cmd_qbt_monitor(cli) -> int:
    """Handle: torrup qbt monitor [--once]."""
    once = getattr(cli.args, "once", False)

    with db() as conn:
        enabled = get_setting(conn, "qbt_enabled") == "1"
        auto_source = get_setting(conn, "qbt_auto_source") == "1"
        if not enabled or not auto_source:
            return cli.error("qBT auto-source is disabled (qbt_enabled/qbt_auto_source).", EXIT_INVALID_ARGS)

    if once:
        from src.auto_worker import qbt_monitor_once
        added = qbt_monitor_once()
        cli.output({"queued": added}, f"Queued {added} item(s) from qBT.")
        return EXIT_SUCCESS

    # Continuous monitor: run the worker loop.
    from src.auto_worker import qbt_monitor_worker

    try:
        qbt_monitor_worker()
    except KeyboardInterrupt:
        return EXIT_SUCCESS
    return EXIT_SUCCESS
