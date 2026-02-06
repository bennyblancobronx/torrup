"""torrup Command Line Interface."""

from __future__ import annotations

import argparse
import json
import sys

from src.config import APP_VERSION, MEDIA_TYPES
from src.db import init_db

from src.cli.browse import cmd_browse
from src.cli.queue import (
    cmd_queue_add,
    cmd_queue_delete,
    cmd_queue_list,
    cmd_queue_run,
    cmd_queue_update,
)
from src.cli.settings import cmd_settings_get, cmd_settings_set
from src.cli.qbt import cmd_qbt_add, cmd_qbt_test
from src.cli.upload import (
    cmd_check_dup,
    cmd_prepare,
    cmd_upload,
    cmd_uploads_list,
    cmd_uploads_show,
)
from src.cli.scan import cmd_scan
from src.cli.activity import cmd_activity

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1


class CLI:
    """torrup CLI handler."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.json_output = getattr(args, "json", False)
        self.quiet = getattr(args, "quiet", False)
        self.verbose = getattr(args, "verbose", False)
        init_db()

    def output(self, data: dict | list | str, message: str = "") -> None:
        """Output data in appropriate format."""
        if self.quiet and not self.json_output:
            return
        if self.json_output:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(message if message else data)

    def error(self, message: str, code: int = EXIT_ERROR) -> int:
        """Output error and return code."""
        if self.json_output:
            print(json.dumps({"error": message}), file=sys.stderr)
        else:
            print(f"Error: {message}", file=sys.stderr)
        return code


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser with all subcommands."""
    parser = argparse.ArgumentParser(prog="torrup", description="torrup - Torrent Upload Tool")
    parser.add_argument("--version", "-v", action="version", version=f"torrup {APP_VERSION}")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress non-essential output")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # settings
    settings_parser = subparsers.add_parser("settings", help="Manage settings")
    settings_sub = settings_parser.add_subparsers(dest="settings_cmd")
    settings_get = settings_sub.add_parser("get", help="Get settings")
    settings_get.add_argument("key", nargs="?", help="Setting key")
    settings_set = settings_sub.add_parser("set", help="Set a setting")
    settings_set.add_argument("key", help="Setting key")
    settings_set.add_argument("value", help="Setting value")

    # browse
    browse_parser = subparsers.add_parser("browse", help="Browse media library")
    browse_parser.add_argument("media_type", choices=MEDIA_TYPES, help="Media type")
    browse_parser.add_argument("path", nargs="?", help="Subdirectory path")
    browse_parser.add_argument("--depth", type=int, default=1, help="Max directory depth")
    browse_parser.add_argument("--show-files", action="store_true", help="Include files")

    # scan
    scan_parser = subparsers.add_parser("scan", help="Scan library for missing uploads")
    scan_parser.add_argument("media_type", choices=MEDIA_TYPES, help="Media type")
    scan_parser.add_argument("path", help="Path to scan")
    scan_parser.add_argument("--recursive", "-r", action="store_true", help="Recursive scan")
    scan_parser.add_argument("--dry-run", action="store_true", help="Identify only, do not queue")

    # queue
    queue_parser = subparsers.add_parser("queue", help="Manage upload queue")
    queue_sub = queue_parser.add_subparsers(dest="queue_cmd")

    queue_add = queue_sub.add_parser("add", help="Add to queue")
    queue_add.add_argument("media_type", choices=MEDIA_TYPES, help="Media type")
    queue_add.add_argument("path", help="Path to media")
    queue_add.add_argument("--category", type=int, help="Category ID")
    queue_add.add_argument("--tags", help="Comma-separated tags")
    queue_add.add_argument("--release-name", help="Override release name")

    queue_list = queue_sub.add_parser("list", help="List queue")
    queue_list.add_argument("--status", help="Filter by status")
    queue_list.add_argument("--media-type", help="Filter by media type")
    queue_list.add_argument("--limit", type=int, default=50, help="Max items")
    queue_list.add_argument("--offset", type=int, default=0, help="Skip items")

    queue_update = queue_sub.add_parser("update", help="Update queue item")
    queue_update.add_argument("id", type=int, help="Queue item ID")
    queue_update.add_argument("--release-name", help="New release name")
    queue_update.add_argument("--category", type=int, help="New category")
    queue_update.add_argument("--tags", help="New tags")
    queue_update.add_argument("--status", help="New status")
    queue_update.add_argument("--approval", choices=["approved", "pending_approval", "rejected"], help="Approval status")

    queue_delete = queue_sub.add_parser("delete", help="Delete from queue")
    queue_delete.add_argument("id", type=int, help="Queue item ID")
    queue_delete.add_argument("--force", action="store_true", help="Skip confirmation")

    queue_run = queue_sub.add_parser("run", help="Run queue worker")
    queue_run.add_argument("--once", action="store_true", help="Process one item and exit")
    queue_run.add_argument("--interval", type=int, default=30, help="Check interval (seconds)")
    queue_run.add_argument("--max-concurrent", type=int, default=1, help="Max concurrent uploads")

    # prepare
    prepare_parser = subparsers.add_parser("prepare", help="Prepare NFO/torrent")
    prepare_parser.add_argument("id", type=int, help="Queue item ID")
    prepare_parser.add_argument("--force", action="store_true", help="Regenerate files")
    prepare_parser.add_argument("--output-dir", help="Output directory")

    # upload
    upload_parser = subparsers.add_parser("upload", help="Upload to TorrentLeech")
    upload_parser.add_argument("id", type=int, help="Queue item ID")
    upload_parser.add_argument("--skip-dup-check", action="store_true", help="Skip duplicate check")
    upload_parser.add_argument("--dry-run", action="store_true", help="Validate only")

    # check-dup
    dup_parser = subparsers.add_parser("check-dup", help="Check for duplicates")
    dup_parser.add_argument("release_name", help="Release name to check")

    # uploads
    uploads_parser = subparsers.add_parser("uploads", help="Upload history")
    uploads_sub = uploads_parser.add_subparsers(dest="uploads_cmd")

    uploads_list = uploads_sub.add_parser("list", help="List upload history")
    uploads_list.add_argument("--status", help="Filter by status")
    uploads_list.add_argument("--media-type", help="Filter by media type")
    uploads_list.add_argument("--limit", type=int, default=50, help="Max items")
    uploads_list.add_argument("--since", help="Items since date (YYYY-MM-DD)")

    uploads_show = uploads_sub.add_parser("show", help="Show upload details")
    uploads_show.add_argument("id", type=int, help="Upload ID")

    # activity
    subparsers.add_parser("activity", help="Show TL activity health for the current month")

    # qbt
    qbt_parser = subparsers.add_parser("qbt", help="qBitTorrent commands")
    qbt_sub = qbt_parser.add_subparsers(dest="qbt_cmd")

    qbt_test = qbt_sub.add_parser("test", help="Test qBitTorrent connection")

    qbt_add = qbt_sub.add_parser("add", help="Add a torrent to qBitTorrent")
    qbt_add.add_argument("--torrent", required=True, help="Path to .torrent file")
    qbt_add.add_argument("--save-path", required=True, help="Path to content data")
    qbt_add.add_argument("--category", help="Optional qBT category")

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return EXIT_SUCCESS

    cli = CLI(args)

    if args.command == "settings":
        if args.settings_cmd == "get":
            return cmd_settings_get(cli)
        elif args.settings_cmd == "set":
            return cmd_settings_set(cli)
        parser.parse_args(["settings", "--help"])
    elif args.command == "browse":
        return cmd_browse(cli)
    elif args.command == "scan":
        return cmd_scan(cli)
    elif args.command == "queue":
        if args.queue_cmd == "add":
            return cmd_queue_add(cli)
        elif args.queue_cmd == "list":
            return cmd_queue_list(cli)
        elif args.queue_cmd == "update":
            return cmd_queue_update(cli)
        elif args.queue_cmd == "delete":
            return cmd_queue_delete(cli)
        elif args.queue_cmd == "run":
            return cmd_queue_run(cli)
        parser.parse_args(["queue", "--help"])
    elif args.command == "prepare":
        return cmd_prepare(cli)
    elif args.command == "upload":
        return cmd_upload(cli)
    elif args.command == "check-dup":
        return cmd_check_dup(cli)
    elif args.command == "activity":
        return cmd_activity(cli)
    elif args.command == "uploads":
        if args.uploads_cmd == "list":
            return cmd_uploads_list(cli)
        elif args.uploads_cmd == "show":
            return cmd_uploads_show(cli)
        parser.parse_args(["uploads", "--help"])
    elif args.command == "qbt":
        if args.qbt_cmd == "test":
            return cmd_qbt_test(cli)
        elif args.qbt_cmd == "add":
            return cmd_qbt_add(cli)
        parser.parse_args(["qbt", "--help"])

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
