"""
TLT - TorrentLeechTool
Simple web UI for creating and uploading torrents to TorrentLeech.
"""
from __future__ import annotations

import os
import threading

from flask import Flask

from src.config import RUN_WORKER
from src.db import init_db
from src.routes import bp
from src.worker import queue_worker

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Register routes
app.register_blueprint(bp)

# Initialize database
init_db()

# Start background worker
if RUN_WORKER:
    t = threading.Thread(target=queue_worker, daemon=True)
    t.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
