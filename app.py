"""
Torrup - Torrent uploader for TorrentLeech
Simple web UI for creating and uploading torrents to TorrentLeech.
"""
from __future__ import annotations

import os
import sys
import threading

from flask import Flask, request, Response
from flask_wtf.csrf import CSRFProtect

from src.config import RUN_WORKER
from src.logger import logger

# Optional basic auth - only enabled if both env vars are set
AUTH_USER = os.environ.get("TORRUP_AUTH_USER")
AUTH_PASS = os.environ.get("TORRUP_AUTH_PASS")
from src.db import init_db
from src.routes import bp
from src.worker import queue_worker

app = Flask(__name__)

# Require SECRET_KEY - fail fast if not set
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    print("ERROR: SECRET_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)
app.secret_key = secret_key
app.config["WTF_CSRF_HEADERS"] = ["X-CSRFToken"]
csrf = CSRFProtect(app)


@app.before_request
def check_auth():
    """Optional basic auth - only if TORRUP_AUTH_USER and TORRUP_AUTH_PASS are set."""
    if AUTH_USER and AUTH_PASS:
        auth = request.authorization
        if not auth or auth.username != AUTH_USER or auth.password != AUTH_PASS:
            return Response(
                "Authentication required",
                401,
                {"WWW-Authenticate": 'Basic realm="Torrup"'},
            )


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Register routes
app.register_blueprint(bp)

# Initialize database
init_db()
logger.info("Database initialized")

# Start background worker
if RUN_WORKER:
    t = threading.Thread(target=queue_worker, daemon=True)
    t.start()
    logger.info("Background worker thread started")

if __name__ == "__main__":
    logger.info("Starting Torrup application on port 5001")
    app.run(host="0.0.0.0", port=5001, debug=False)
