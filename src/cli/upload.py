"""Upload CLI commands (prepare, upload, check-dup, uploads)."""

from __future__ import annotations

from pathlib import Path

from src.api import check_exists, upload_torrent
from src.db import db, get_output_dir, get_setting
from src.utils import (
    create_torrent,
    extract_metadata,
    extract_thumbnail,
    generate_nfo,
    get_folder_size,
    now_iso,
    sanitize_release_name,
    write_xml_metadata,
)
from src.worker import update_queue_status

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_NOT_FOUND = 3
EXIT_DUPLICATE = 4
EXIT_API_ERROR = 5
EXIT_MISSING_DEP = 6


def cmd_prepare(cli) -> int:
    """Handle: torrup prepare <id>."""
    item_id = cli.args.id
    force = getattr(cli.args, "force", False)
    output_dir = getattr(cli.args, "output_dir", None)

    with db() as conn:
        row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return cli.error(f"Queue item not found: {item_id}", EXIT_NOT_FOUND)

        path = Path(row["path"])
        if not path.exists():
            return cli.error(f"Path not found: {path}", EXIT_NOT_FOUND)

        release_name = sanitize_release_name(row["release_name"])
        out_dir = Path(output_dir) if output_dir else get_output_dir(conn)
        release_group = get_setting(conn, "release_group") or "Torrup"
        media_type = row["media_type"]
        tags = row["tags"]

        nfo_path = out_dir / f"{release_name}.nfo"
        torrent_path = out_dir / f"{release_name}.torrent"

        if not force and nfo_path.exists() and torrent_path.exists():
            cli.output({"id": item_id, "status": "exists"}, "Files already exist (use --force to regenerate)")
            return EXIT_SUCCESS

        try:
            metadata = extract_metadata(path, media_type)
            thumb_path = extract_thumbnail(path, out_dir, release_name, media_type)
            nfo = generate_nfo(path, release_name, out_dir, media_type, release_group, metadata)
            torrent = create_torrent(path, release_name, out_dir)
            size_bytes = get_folder_size(path) if path.is_dir() else path.stat().st_size
            xml = write_xml_metadata(
                release_name, media_type, path, size_bytes, torrent, nfo, tags, out_dir, metadata, thumb_path
            )

            conn.execute(
                "UPDATE queue SET torrent_path=?, nfo_path=?, xml_path=?, thumb_path=?, updated_at=? WHERE id=?",
                (str(torrent), str(nfo), str(xml), str(thumb_path) if thumb_path else None, now_iso(), item_id),
            )
            conn.commit()

            cli.output(
                {"nfo": str(nfo), "torrent": str(torrent), "xml": str(xml)},
                f"Prepared: {release_name}\n  NFO: {nfo}\n  Torrent: {torrent}\n  XML: {xml}",
            )
        except FileNotFoundError as e:
            if "mktorrent" in str(e) or "mediainfo" in str(e):
                return cli.error(f"Missing dependency: {e}", EXIT_MISSING_DEP)
            return cli.error(str(e), EXIT_ERROR)
        except Exception as e:
            return cli.error(str(e), EXIT_ERROR)

    return EXIT_SUCCESS


def cmd_upload(cli) -> int:
    """Handle: torrup upload <id>."""
    item_id = cli.args.id
    skip_dup = getattr(cli.args, "skip_dup_check", False)
    dry_run = getattr(cli.args, "dry_run", False)

    with db() as conn:
        row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return cli.error(f"Queue item not found: {item_id}", EXIT_NOT_FOUND)

        release_name = row["release_name"]
        torrent_path = row["torrent_path"]
        nfo_path = row["nfo_path"]
        category = row["category"]
        tags = row["tags"]

        if not torrent_path or not nfo_path:
            return cli.error("Item not prepared. Run 'torrup prepare' first.", EXIT_ERROR)

        if not skip_dup and check_exists(release_name):
            update_queue_status(conn, item_id, "duplicate", "Duplicate found on TorrentLeech")
            conn.commit()
            return cli.error(f"Duplicate found: {release_name}", EXIT_DUPLICATE)

        if dry_run:
            cli.output({"id": item_id, "dry_run": True}, f"Dry run: would upload {release_name}")
            return EXIT_SUCCESS

        try:
            result = upload_torrent(Path(torrent_path), Path(nfo_path), category, tags)
            if result.get("success"):
                update_queue_status(conn, item_id, "success", f"Uploaded: {result['torrent_id']}")
                conn.commit()
                cli.output(result, f"Uploaded: torrent_id={result['torrent_id']}")
                return EXIT_SUCCESS
            else:
                update_queue_status(conn, item_id, "failed", result.get("error", "Unknown error"))
                conn.commit()
                return cli.error(result.get("error", "Upload failed"), EXIT_API_ERROR)
        except Exception as e:
            return cli.error(str(e), EXIT_API_ERROR)


def cmd_check_dup(cli) -> int:
    """Handle: torrup check-dup <release_name>."""
    release_name = cli.args.release_name
    try:
        exists = check_exists(release_name)
        if exists:
            cli.output({"duplicate": True, "release_name": release_name}, f"Duplicate found: {release_name}")
            return EXIT_DUPLICATE
        else:
            cli.output({"duplicate": False, "release_name": release_name}, f"No duplicate found for: {release_name}")
            return EXIT_SUCCESS
    except Exception as e:
        return cli.error(str(e), EXIT_API_ERROR)


def cmd_uploads_list(cli) -> int:
    """Handle: torrup uploads list."""
    status = getattr(cli.args, "status", None)
    media_type = getattr(cli.args, "media_type", None)
    limit = getattr(cli.args, "limit", 50)
    since = getattr(cli.args, "since", None)

    query = "SELECT * FROM queue WHERE status IN ('success', 'failed', 'duplicate')"
    params = []

    if status:
        query = "SELECT * FROM queue WHERE status = ?"
        params = [status]
    if media_type:
        query += " AND media_type = ?"
        params.append(media_type)
    if since:
        query += " AND created_at >= ?"
        params.append(since)

    query += " ORDER BY updated_at DESC LIMIT ?"
    params.append(limit)

    with db() as conn:
        rows = conn.execute(query, params).fetchall()
        items = [dict(r) for r in rows]

    if cli.json_output:
        cli.output(items)
    else:
        if not items:
            print("No upload history")
        for item in items:
            print(f"[{item['id']}] {item['status']:10} {item['release_name']}")
    return EXIT_SUCCESS


def cmd_uploads_show(cli) -> int:
    """Handle: torrup uploads show <id>."""
    item_id = cli.args.id
    with db() as conn:
        row = conn.execute("SELECT * FROM queue WHERE id = ?", (item_id,)).fetchone()
        if not row:
            return cli.error(f"Upload not found: {item_id}", EXIT_NOT_FOUND)

        item = dict(row)
        if cli.json_output:
            cli.output(item)
        else:
            for k, v in item.items():
                print(f"{k}: {v}")
    return EXIT_SUCCESS
