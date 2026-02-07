"""Changelog page route handler."""

from __future__ import annotations

import re
from pathlib import Path

from flask import render_template

from src.config import APP_NAME, APP_VERSION
from src.routes import bp


@bp.route("/changelog")
def changelog() -> str:
    """Changelog page - renders CHANGELOG.md as styled HTML."""
    changelog_path = Path(__file__).resolve().parent.parent / "CHANGELOG.md"
    versions = []
    if changelog_path.exists():
        text = changelog_path.read_text(encoding="utf-8")
        # Split into version blocks by ## [x.y.z] headers
        blocks = re.split(r'^## ', text, flags=re.MULTILINE)
        for block in blocks[1:]:  # skip preamble before first ##
            lines = block.strip().split('\n')
            header = lines[0]
            # Parse version and date from "[0.1.9] - 2026-02-06"
            match = re.match(r'\[([^\]]+)\]\s*-\s*(.+)', header)
            if not match:
                continue
            version = match.group(1)
            date = match.group(2).strip()
            # Parse subsections (### Added, ### Changed, etc.)
            sections = []
            current_section = None
            for line in lines[1:]:
                if line.startswith('### '):
                    current_section = {"title": line[4:].strip(), "items": []}
                    sections.append(current_section)
                elif line.startswith('- ') and current_section is not None:
                    current_section["items"].append(line[2:])
                elif line.startswith('  ') and current_section and current_section["items"]:
                    # Continuation of previous bullet (indented sub-item)
                    current_section["items"][-1] += '\n' + line
            versions.append({"version": version, "date": date, "sections": sections})
    return render_template(
        "changelog.html",
        app_name=APP_NAME,
        app_version=APP_VERSION,
        versions=versions,
    )
