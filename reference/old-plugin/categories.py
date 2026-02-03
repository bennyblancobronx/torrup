"""TorrentLeech category mapping.

Based on official TorrentLeech documentation.
"""

from typing import Any

from barbossa.core.models import ContentType

# TV Categories
CAT_EPISODES_SD = 26
CAT_EPISODES_HD = 32
CAT_BOXSETS = 27
CAT_TV_FOREIGN = 44

# Movie Categories
CAT_CAM = 8
CAT_TS_TC = 9
CAT_HDRIP = 43
CAT_DVDRIP = 11
CAT_DVD_R = 12
CAT_WEBRIP = 37
CAT_BLURAY_RIP = 14
CAT_BLURAY = 13
CAT_4K = 47
CAT_MOVIE_BOXSETS = 15
CAT_DOCUMENTARIES = 29
CAT_MOVIE_FOREIGN = 36

# Music Categories
CAT_AUDIO = 31
CAT_MUSIC_VIDEOS = 16

# Book Categories
CAT_EBOOKS = 45
CAT_COMICS = 46


def get_tv_category(
    resolution: str | None,
    is_season_pack: bool,
    is_foreign: bool,
) -> int:
    """
    Get TV category based on metadata.

    Category hierarchy per TL rules:
    1. Foreign (non-English primary audio)
    2. Boxsets (season packs)
    3. HD/SD by resolution
    """
    if is_foreign:
        return CAT_TV_FOREIGN

    if is_season_pack:
        return CAT_BOXSETS

    # HD is 720p or higher
    hd_resolutions = {"720p", "1080p", "1080i", "2160p", "4k", "uhd"}
    if resolution and resolution.lower() in hd_resolutions:
        return CAT_EPISODES_HD

    return CAT_EPISODES_SD


def get_movie_category(
    resolution: str | None,
    source: str | None,
    is_remux: bool,
    is_foreign: bool,
    is_documentary: bool,
    is_boxset: bool,
) -> int:
    """
    Get movie category based on metadata.

    Category hierarchy per TL rules:
    1. Foreign (non-English primary audio)
    2. Documentaries
    3. Boxsets (multi-movie collections)
    4. 4K
    5. Source-based category
    """
    if is_foreign:
        return CAT_MOVIE_FOREIGN

    if is_documentary:
        return CAT_DOCUMENTARIES

    if is_boxset:
        return CAT_MOVIE_BOXSETS

    # 4K content
    if resolution and resolution.lower() in {"2160p", "4k", "uhd"}:
        return CAT_4K

    # Source-based categorization
    if source:
        source_lower = source.lower()

        if "cam" in source_lower:
            return CAT_CAM
        if source_lower in {"ts", "tc", "telesync", "telecine"}:
            return CAT_TS_TC
        if "hdrip" in source_lower:
            return CAT_HDRIP
        if source_lower in {"dvdscr", "dvdscreener"}:
            return CAT_DVDRIP
        if source_lower in {"dvdrip", "dvd-rip"}:
            return CAT_DVDRIP
        if source_lower in {"dvd-r", "dvd", "dvd9", "dvd5"}:
            return CAT_DVD_R
        if source_lower in {"web-dl", "webdl", "webrip", "web"}:
            return CAT_WEBRIP
        if source_lower in {"blu-ray", "bluray", "bdrip", "brrip"}:
            if is_remux:
                return CAT_BLURAY
            return CAT_BLURAY_RIP

    # Default to BlurayRip for unknown
    return CAT_BLURAY_RIP


def map_category(
    content_type: ContentType,
    metadata: dict[str, Any],
) -> int:
    """
    Map content type and metadata to TorrentLeech category.

    Args:
        content_type: Type of content
        metadata: Additional metadata

    Returns:
        Category ID
    """
    resolution = metadata.get("resolution")
    source = metadata.get("source")
    is_foreign = metadata.get("is_foreign", False)
    is_documentary = metadata.get("is_documentary", False)
    is_remux = "remux" in metadata.get("release_name", "").lower()

    if content_type == ContentType.TV_EPISODE:
        return get_tv_category(resolution, is_season_pack=False, is_foreign=is_foreign)

    if content_type == ContentType.TV_SEASON:
        return get_tv_category(resolution, is_season_pack=True, is_foreign=is_foreign)

    if content_type == ContentType.MOVIE:
        return get_movie_category(
            resolution=resolution,
            source=source,
            is_remux=is_remux,
            is_foreign=is_foreign,
            is_documentary=is_documentary,
            is_boxset=metadata.get("is_boxset", False),
        )

    if content_type == ContentType.MUSIC:
        # Check if it has video
        if metadata.get("has_video", False):
            return CAT_MUSIC_VIDEOS
        return CAT_AUDIO

    if content_type == ContentType.EBOOK:
        return CAT_EBOOKS

    if content_type == ContentType.COMIC:
        return CAT_COMICS

    # Default to Episodes HD for unknown video content
    return CAT_EPISODES_HD
