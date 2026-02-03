"""TorrentLeech API client."""

from pathlib import Path
from typing import Any

import httpx

UPLOAD_URL = "https://www.torrentleech.org/torrents/upload/apiupload"
DOWNLOAD_URL = "https://www.torrentleech.org/torrents/upload/apidownload"
SEARCH_URL = "https://www.torrentleech.org/api/torrentsearch"


class TorrentLeechAPI:
    """Client for TorrentLeech API."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize API client.

        Args:
            api_key: TorrentLeech announce key (32 characters)
        """
        self.api_key = api_key
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "TorrentLeechAPI":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=60.0)
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get HTTP client."""
        if self._client is None:
            raise RuntimeError("API client not initialized. Use async with.")
        return self._client

    async def upload(
        self,
        torrent_path: Path,
        category: int,
        nfo_path: Path | None = None,
        description: str | None = None,
        imdb: str | None = None,
        tvmaze_id: int | None = None,
        tvmaze_type: int | None = None,
        tags: str | None = None,
    ) -> str:
        """
        Upload torrent to TorrentLeech.

        Args:
            torrent_path: Path to .torrent file
            category: Category ID
            nfo_path: Path to NFO file (optional)
            description: NFO text (alternative to file)
            imdb: IMDB ID (e.g., "tt1234567")
            tvmaze_id: TVMaze show ID
            tvmaze_type: 1 for series, 2 for episode
            tags: Comma-separated tags

        Returns:
            Torrent ID on success

        Raises:
            Exception: On upload failure
        """
        files: dict[str, Any] = {
            "torrent": (torrent_path.name, torrent_path.read_bytes()),
        }

        data: dict[str, Any] = {
            "announcekey": self.api_key,
            "category": str(category),
        }

        # NFO - either file or text
        if nfo_path and nfo_path.exists():
            files["nfo"] = (nfo_path.name, nfo_path.read_bytes())
        elif description:
            data["description"] = description

        # Optional metadata
        if imdb:
            data["imdb"] = imdb
        if tvmaze_id is not None:
            data["tvmazeid"] = str(tvmaze_id)
            if tvmaze_type is not None:
                data["tvmazetype"] = str(tvmaze_type)
        if tags:
            data["tags"] = tags

        response = await self.client.post(
            UPLOAD_URL,
            data=data,
            files=files,
        )

        result = response.text.strip()

        # Success returns numeric torrent ID
        if result.isdigit():
            return result

        # Error returns text message
        raise Exception(f"Upload failed: {result}")

    async def download(self, torrent_id: str) -> bytes:
        """
        Download .torrent file.

        Args:
            torrent_id: Torrent ID

        Returns:
            Torrent file bytes
        """
        response = await self.client.post(
            DOWNLOAD_URL,
            data={
                "announcekey": self.api_key,
                "torrentID": torrent_id,
            },
        )

        if response.status_code != 200:
            raise Exception(f"Download failed: {response.status_code}")

        return response.content

    async def search(self, query: str, exact: bool = False) -> bool:
        """
        Search for existing torrent.

        Args:
            query: Search query (release name)
            exact: Whether to do exact match

        Returns:
            True if torrent exists (is a duplicate)
        """
        data: dict[str, Any] = {
            "announcekey": self.api_key,
            "query": f"'{query}'",  # Single quotes required per API docs
        }

        if exact:
            data["exact"] = "1"

        response = await self.client.post(SEARCH_URL, data=data)
        result = response.text.strip()

        # 0 = not found, 1 = found
        return result == "1"
