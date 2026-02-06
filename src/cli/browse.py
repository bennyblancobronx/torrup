"""Browse CLI command."""

from __future__ import annotations

from pathlib import Path

from src.config import MEDIA_TYPES
from src.db import db, get_excludes, get_media_roots
from src.utils import is_excluded

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 2
EXIT_NOT_FOUND = 3


def cmd_browse(cli) -> int:
    """Handle: torrup browse <media_type> [path]."""
    media_type = cli.args.media_type
    subpath = getattr(cli.args, "path", None)
    show_files = getattr(cli.args, "show_files", False)

    if media_type not in MEDIA_TYPES:
        return cli.error(f"Invalid media type: {media_type}. Use: {', '.join(MEDIA_TYPES)}", EXIT_INVALID_ARGS)

    with db() as conn:
        roots = {r["media_type"]: r for r in get_media_roots(conn)}
        excludes = get_excludes(conn)

    root_info = roots.get(media_type)
    if not root_info:
        return cli.error(f"No root configured for {media_type}", EXIT_NOT_FOUND)

    base_path = Path(root_info["path"])
    if subpath:
        base_path = base_path / subpath

    if not base_path.exists():
        return cli.error(f"Path not found: {base_path}", EXIT_NOT_FOUND)

    items = []
    for entry in sorted(base_path.iterdir()):
        if is_excluded(entry, excludes):
            continue
        if entry.is_dir():
            items.append({
                "name": entry.name,
                "path": str(entry),
                "type": "dir",
                "modified": entry.stat().st_mtime,
            })
        elif show_files and entry.is_file():
            items.append({
                "name": entry.name,
                "path": str(entry),
                "type": "file",
                "size": entry.stat().st_size,
                "modified": entry.stat().st_mtime,
            })

    if cli.json_output:
        cli.output(items)
    else:
        for item in items:
            prefix = "[D]" if item["type"] == "dir" else "[F]"
            print(f"{prefix} {item['name']}")
    return EXIT_SUCCESS
