"""CLI command for activity health check."""

from __future__ import annotations

from src.db import db
from src.utils.activity import calculate_health


def cmd_activity(cli) -> int:
    """Show TorrentLeech activity health for the current month."""
    with db() as conn:
        health = calculate_health(conn)

    if cli.json_output:
        cli.output(health)
        return 0

    lines = [
        f"Uploads this month: {health['uploads']}",
        f"Queued:             {health['queued']}",
        f"Projected:          {health['projected']} / {health['minimum']}",
        f"Needed:             {health['needed']}",
        f"Days remaining:     {health['days_remaining']}",
        f"Enforce:            {'yes' if health['enforce'] else 'no'}",
    ]

    if health["pace"] is not None:
        lines.append(f"Pace (7d avg):      {health['pace']}/day")

    if health["critical"]:
        lines.append("")
        lines.append("WARNING: Projected uploads are below the monthly minimum.")

    cli.output("\n".join(lines), "\n".join(lines))
    return 0
