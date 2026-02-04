"""Logging configuration for Torrup."""

from __future__ import annotations

import logging
import os


def setup_logging() -> logging.Logger:
    """Configure and return the application logger."""
    level = logging.DEBUG if os.environ.get("FLASK_DEBUG") == "true" else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger('torrup')


logger = setup_logging()
