"""Settings CLI commands."""

from __future__ import annotations

from src.db import db, get_setting, set_setting

# Exit codes
EXIT_SUCCESS = 0
EXIT_NOT_FOUND = 3


def cmd_settings_get(cli) -> int:
    """Handle: torrup settings get [key]."""
    key = getattr(cli.args, "key", None)
    with db() as conn:
        if key:
            value = get_setting(conn, key)
            if not value and key not in ("output_dir", "exclude_dirs", "release_group"):
                return cli.error(f"Setting not found: {key}", EXIT_NOT_FOUND)
            cli.output({"key": key, "value": value}, value)
        else:
            settings = {}
            for row in conn.execute("SELECT key, value FROM settings").fetchall():
                settings[row["key"]] = row["value"]
            if cli.json_output:
                cli.output(settings)
            else:
                for k, v in sorted(settings.items()):
                    print(f"{k}: {v}")
    return EXIT_SUCCESS


def cmd_settings_set(cli) -> int:
    """Handle: torrup settings set <key> <value>."""
    key = cli.args.key
    value = cli.args.value
    with db() as conn:
        set_setting(conn, key, value)
        conn.commit()
    cli.output({"key": key, "value": value}, f"Set {key} = {value}")
    return EXIT_SUCCESS
