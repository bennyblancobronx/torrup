FROM python:3.14.2-slim

LABEL maintainer="project-maintainer" \
      version="0.1.0" \
      description="Torrup - Torrent uploader for TorrentLeech"

RUN apt-get update && apt-get install -y --no-install-recommends \
    mediainfo \
    mktorrent \
    curl \
    libimage-exiftool-perl \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY src ./src/
COPY templates ./templates/

RUN mkdir -p /app/data /app/output \
  && chown -R appuser:appuser /app

USER appuser

ENV TORRUP_RUN_WORKER=1 \
    TORRUP_DB_PATH=/app/data/torrup.db \
    TORRUP_OUTPUT_DIR=/app/output

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5001/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "1", "app:app"]
