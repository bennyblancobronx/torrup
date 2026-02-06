FROM python:3.11.7-slim

LABEL maintainer="project-maintainer" \
      version="0.1.8" \
      description="torrup - Torrent Upload Tool"

RUN apt-get update && apt-get install -y --no-install-recommends \
    mediainfo \
    mktorrent \
    curl \
    libimage-exiftool-perl \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash appuser
RUN mkdir -p /app/data /app/output && chown appuser:appuser /app /app/data /app/output

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER appuser

COPY --chown=appuser:appuser app.py ./
COPY --chown=appuser:appuser src ./src/
COPY --chown=appuser:appuser templates ./templates/
COPY --chown=appuser:appuser static ./static/

ENV TORRUP_RUN_WORKER=1 \
    TORRUP_DB_PATH=/app/data/torrup.db \
    TORRUP_OUTPUT_DIR=/app/output \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD curl -fsS http://localhost:5001/health || exit 1

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5001", \
     "--workers", "1", \
     "--worker-class", "gthread", \
     "--threads", "8", \
     "--timeout", "180", \
     "--access-logfile", "-", \
     "app:app"]
