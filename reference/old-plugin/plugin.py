"""TorrentLeech plugin implementation."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, SecretStr

from barbossa.core.models import ContentType
from barbossa.plugins.base import TrackerPlugin, UploadResult
from barbossa.plugins.torrentleech.api import TorrentLeechAPI
from barbossa.plugins.torrentleech.categories import map_category


class TorrentLeechSettings(BaseModel):
    """TorrentLeech plugin settings.

    Only requires the Torrent Passkey from your TL profile.
    This single key is used for both API authentication and torrent announces.
    Location: TorrentLeech → Profile → "Torrent Passkey"
    """

    passkey: SecretStr  # 32-char Torrent Passkey from profile
    announce_url: str = "https://tracker.torrentleech.org"


class TorrentLeechPlugin(TrackerPlugin):
    """TorrentLeech tracker plugin."""

    name = "torrentleech"
    version = "1.0.0"

    def __init__(self, settings: TorrentLeechSettings) -> None:
        """
        Initialize plugin with settings.

        Args:
            settings: Plugin settings
        """
        self.settings = settings

    def get_settings_schema(self) -> type[BaseModel]:
        """Return settings schema."""
        return TorrentLeechSettings

    def validate_settings(self, settings: BaseModel) -> bool:
        """Validate settings."""
        if not isinstance(settings, TorrentLeechSettings):
            return False

        # Check passkey format (32 hex characters)
        passkey = settings.passkey.get_secret_value()
        return len(passkey) == 32

    def map_category(self, content_type: ContentType, metadata: dict[str, Any]) -> int:
        """Map content to category ID."""
        return map_category(content_type, metadata)

    def get_required_fields(self, content_type: ContentType) -> list[str]:
        """
        Get required fields for upload.

        Per TorrentLeech API, only category and torrent are required.
        IMDB/TVMaze are optional but recommended.
        """
        required = ["category"]

        if content_type == ContentType.MOVIE:
            # IMDB recommended for movies
            required.append("imdb")
        elif content_type in (ContentType.TV_EPISODE, ContentType.TV_SEASON):
            # TVMaze recommended for TV
            required.append("tvmaze_id")

        return required

    def get_announce_url(self) -> str:
        """Get announce URL."""
        return self.settings.announce_url

    def get_source_tag(self) -> str:
        """
        Get source tag for torrent.

        Must be exactly "TorrentLeech.org" per TL documentation.
        """
        return "TorrentLeech.org"

    async def upload(
        self,
        torrent_path: Path,
        nfo_path: Path | None,
        metadata: dict[str, Any],
    ) -> UploadResult:
        """Upload torrent to TorrentLeech."""
        passkey = self.settings.passkey.get_secret_value()

        try:
            async with TorrentLeechAPI(passkey) as api:
                # Check for duplicates first
                release_name = torrent_path.stem
                if await api.search(release_name, exact=True):
                    return UploadResult(
                        success=False,
                        error=f"Duplicate exists: {release_name}",
                    )

                # Upload
                torrent_id = await api.upload(
                    torrent_path=torrent_path,
                    category=metadata["category"],
                    nfo_path=nfo_path,
                    imdb=metadata.get("imdb"),
                    tvmaze_id=metadata.get("tvmaze_id"),
                    tvmaze_type=metadata.get("tvmaze_type"),
                    tags=metadata.get("tags"),
                )

                return UploadResult(
                    success=True,
                    torrent_id=torrent_id,
                    download_url=f"https://www.torrentleech.org/torrent/{torrent_id}",
                )

        except Exception as e:
            return UploadResult(
                success=False,
                error=str(e),
            )

    async def download_torrent(self, torrent_id: str) -> bytes:
        """Download torrent file after upload."""
        passkey = self.settings.passkey.get_secret_value()

        async with TorrentLeechAPI(passkey) as api:
            return await api.download(torrent_id)

    async def search(self, query: str, exact: bool = False) -> bool:
        """Search for existing torrent."""
        passkey = self.settings.passkey.get_secret_value()

        async with TorrentLeechAPI(passkey) as api:
            return await api.search(query, exact)
