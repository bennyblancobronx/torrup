"""NFO generation utilities."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

from src.config import NFO_TEMPLATES
from src.logger import logger
from src.utils.core import get_folder_size, human_size, validate_path_for_subprocess


def generate_nfo(
    path: Path,
    release_name: str,
    out_dir: Path,
    media_type: str = "movies",
    release_group: str = "torrup",
    metadata: dict | None = None,
) -> Path:
    """Generate NFO file using template and mediainfo."""
    nfo_path = out_dir / f"{release_name}.nfo"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata = metadata or {}

    # Get mediainfo for audio/video files
    media_extensions = {".flac", ".mp3", ".m4a", ".mkv", ".mp4", ".avi", ".m4v"}
    media_file = None
    if path.is_file() and path.suffix.lower() in media_extensions:
        media_file = path
    else:
        for f in path.rglob("*"):
            if f.suffix.lower() in media_extensions:
                media_file = f
                break

    mediainfo = ""
    if media_file and validate_path_for_subprocess(media_file):
        try:
            result = subprocess.run(
                ["mediainfo", str(media_file)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            path_indicators = ("complete name", "file name", "folder name")
            filtered_lines = []
            for line in result.stdout.split("\n"):
                stripped = line.strip().lower()
                if any(stripped.startswith(ind) for ind in path_indicators):
                    continue
                if " : /" in line or " : C:\\" in line:
                    continue
                filtered_lines.append(line)
            mediainfo = "\n".join(filtered_lines)
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
            logger.warning("mediainfo binary not found -- container may need rebuild")
            mediainfo = "  MediaInfo not available"

    # Count files and calculate size for books
    file_count = sum(1 for f in path.rglob("*") if f.is_file()) if path.is_dir() else 1
    try:
        size_bytes = get_folder_size(path) if path.is_dir() else path.stat().st_size
    except ValueError as e:
        raise ValueError(f"Cannot generate NFO: {e}") from e

    # Extract info from release name for template (use metadata if available)
    source = _extract_source(release_name)
    resolution = _extract_resolution(release_name)
    file_format = _extract_format(release_name, path)

    # Build metadata section if we have extracted data
    metadata_section = _format_metadata_section(metadata, media_type)
    basic_info = ""
    audio_details = ""
    lyrics_section = ""
    album_art_section = ""
    if media_type == "music" and metadata:
        basic_info = _format_music_basic_info(metadata)
        audio_details = _format_audio_details(metadata)
        lyrics_section = _format_lyrics_section(metadata)
        art = metadata.get("album_art")
        art_lines = []
        if art:
            art_lines.append(
                f"  Embedded Art   : {art.get('format', 'image')}, {art.get('size', 'unknown size')}"
            )
        art_file = metadata.get("album_art_file")
        if art_file:
            art_lines.append(
                f"  Extracted Art  : {art_file.get('name', 'artwork')}, {art_file.get('size', 'unknown size')}"
            )
        album_art_section = "\n".join(art_lines)

    # Get template
    template = NFO_TEMPLATES.get(media_type, NFO_TEMPLATES["movies"])

    # Fill template
    nfo_content = template.format(
        release_name=release_name,
        release_group=release_group,
        source=source,
        resolution=resolution,
        format=file_format,
        mediainfo=mediainfo.strip() if mediainfo else "  No media info available",
        file_count=file_count,
        size=human_size(size_bytes),
        timestamp=timestamp,
        basic_info=basic_info,
        audio_details=audio_details,
        lyrics_section=lyrics_section,
        album_art_section=album_art_section,
    )

    # Clean empty optional sections for music (remove headers if body empty)
    if media_type == "music":
        nfo_content = _strip_empty_section(nfo_content, "BASIC INFO", basic_info)
        nfo_content = _strip_empty_section(nfo_content, "AUDIO DETAILS", audio_details)
        nfo_content = _strip_empty_section(nfo_content, "LYRICS", lyrics_section)
        nfo_content = _strip_empty_section(nfo_content, "ALBUM ART", album_art_section)

    # Insert metadata section before technical info if available
    if metadata_section:
        info_header = "TECHNICAL INFO" if media_type == "music" else "MEDIA INFO"
        nfo_content = nfo_content.replace(
            info_header,
            f"METADATA\n{'-' * 80}\n{metadata_section}\n{'-' * 80}\n{info_header:^80}"
        )

    nfo_path.write_text(nfo_content)
    return nfo_path


def _format_metadata_section(metadata: dict, media_type: str) -> str:
    """Format extracted metadata for NFO display."""
    if not metadata:
        return ""

    lines = []
    if media_type in ("movies", "tv"):
        if metadata.get("title"):
            lines.append(f"  Title          : {metadata['title']}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("description"):
            desc = metadata["description"][:100] + "..." if len(metadata.get("description", "")) > 100 else metadata.get("description", "")
            lines.append(f"  Description    : {desc}")
        if media_type == "tv":
            if metadata.get("show"):
                lines.append(f"  Show           : {metadata['show']}")
            if metadata.get("season"):
                lines.append(f"  Season         : {metadata['season']}")
            if metadata.get("episode"):
                lines.append(f"  Episode        : {metadata['episode']}")

    elif media_type == "music":
        if metadata.get("artist"):
            lines.append(f"  Artist         : {metadata['artist']}")
        if metadata.get("album_artist") and metadata.get("album_artist") != metadata.get("artist"):
            lines.append(f"  Album Artist   : {metadata['album_artist']}")
        if metadata.get("album"):
            lines.append(f"  Album          : {metadata['album']}")
        if metadata.get("track"):
            lines.append(f"  Track          : {metadata['track']}")
        if metadata.get("track_number"):
            track_total = metadata.get("track_total")
            track_val = f"{metadata['track_number']}/{track_total}" if track_total else str(metadata['track_number'])
            lines.append(f"  Track No.      : {track_val}")
        if metadata.get("disc_number"):
            disc_total = metadata.get("disc_total")
            disc_val = f"{metadata['disc_number']}/{disc_total}" if disc_total else str(metadata['disc_number'])
            lines.append(f"  Disc No.       : {disc_val}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("genre"):
            lines.append(f"  Genre          : {metadata['genre']}")
        if metadata.get("label"):
            lines.append(f"  Label          : {metadata['label']}")
        if metadata.get("catalog"):
            lines.append(f"  Catalog        : {metadata['catalog']}")
        if metadata.get("isrc"):
            lines.append(f"  ISRC           : {metadata['isrc']}")
        if metadata.get("composer"):
            lines.append(f"  Composer       : {metadata['composer']}")
        if metadata.get("format"):
            lines.append(f"  Format         : {metadata['format']}")
        if metadata.get("bitrate"):
            lines.append(f"  Bitrate        : {metadata['bitrate']}")
        if metadata.get("bitrate_kbps"):
            lines.append(f"  Bitrate (kbps) : {metadata['bitrate_kbps']}")
        if metadata.get("sample_rate"):
            lines.append(f"  Sample Rate    : {metadata['sample_rate']}")
        if metadata.get("bit_depth"):
            lines.append(f"  Bit Depth      : {metadata['bit_depth']} bit")
        if metadata.get("channels"):
            lines.append(f"  Channels       : {metadata['channels']}")
        if metadata.get("encoder"):
            lines.append(f"  Encoder        : {metadata['encoder']}")
        if metadata.get("embedded_lyrics"):
            lines.append("  Embedded Lyrics: Yes")

    elif media_type == "books":
        if metadata.get("title"):
            lines.append(f"  Title          : {metadata['title']}")
        if metadata.get("author"):
            lines.append(f"  Author         : {metadata['author']}")
        if metadata.get("publisher"):
            lines.append(f"  Publisher      : {metadata['publisher']}")
        if metadata.get("year"):
            lines.append(f"  Year           : {metadata['year']}")
        if metadata.get("isbn"):
            lines.append(f"  ISBN           : {metadata['isbn']}")

    return "\n".join(lines)


def _format_music_basic_info(metadata: dict) -> str:
    """Minimum useful music fields for TL NFOs."""
    lines = []
    if metadata.get("artist"):
        lines.append(f"  Artist         : {metadata['artist']}")
    if metadata.get("album"):
        lines.append(f"  Album          : {metadata['album']}")
    if metadata.get("year"):
        lines.append(f"  Year           : {metadata['year']}")
    if metadata.get("genre"):
        lines.append(f"  Genre          : {metadata['genre']}")
    if metadata.get("track"):
        lines.append(f"  Track          : {metadata['track']}")
    if metadata.get("track_number"):
        track_total = metadata.get("track_total")
        track_val = f"{metadata['track_number']}/{track_total}" if track_total else str(metadata['track_number'])
        lines.append(f"  Track No.      : {track_val}")
    if metadata.get("disc_number"):
        disc_total = metadata.get("disc_total")
        disc_val = f"{metadata['disc_number']}/{disc_total}" if disc_total else str(metadata['disc_number'])
        lines.append(f"  Disc No.       : {disc_val}")
    return "\n".join(lines)


def _format_audio_details(metadata: dict) -> str:
    """Format technical audio fields for a compact section."""
    lines = []
    if metadata.get("format"):
        lines.append(f"  Format         : {metadata['format']}")
    if metadata.get("bitrate"):
        lines.append(f"  Bitrate        : {metadata['bitrate']}")
    if metadata.get("bitrate_kbps"):
        lines.append(f"  Bitrate (kbps) : {metadata['bitrate_kbps']}")
    if metadata.get("sample_rate"):
        lines.append(f"  Sample Rate    : {metadata['sample_rate']}")
    if metadata.get("bit_depth"):
        lines.append(f"  Bit Depth      : {metadata['bit_depth']} bit")
    if metadata.get("channels"):
        lines.append(f"  Channels       : {metadata['channels']}")
    if metadata.get("encoder"):
        lines.append(f"  Encoder        : {metadata['encoder']}")
    return "\n".join(lines)


def _format_lyrics_section(metadata: dict) -> str:
    """Format local lyrics file summary if present."""
    if not metadata.get("lyrics"):
        return ""
    lines = []
    total = metadata.get("lyrics_count")
    if total:
        lines.append(f"  Lyrics Files   : {total}")
    for entry in metadata.get("lyrics", []):
        track = entry.get("track")
        lang = entry.get("lang")
        if track and lang:
            lines.append(f"  {track} ({lang})")
        elif track:
            lines.append(f"  {track}")
    return "\n".join(lines)


def _strip_empty_section(nfo: str, title: str, body: str) -> str:
    """Remove a section if its body is empty or whitespace."""
    if body and body.strip():
        return nfo
    header = (
        "--------------------------------------------------------------------------------\n"
        f"{title:^80}\n"
        "--------------------------------------------------------------------------------\n"
    )
    return nfo.replace(header, "")


def _extract_source(name: str) -> str:
    """Extract source type from release name."""
    sources = [
        "BluRay", "Bluray", "REMUX", "WEB-DL", "WEBDL", "WEBRip", "WEBRIP",
        "HDTV", "DVDRip", "DVD-R", "DVDR", "BDRip", "HDRip", "CAM", "TS", "TC",
        "CD", "WEB", "Vinyl", "SACD",
    ]
    name_upper = name.upper()
    for src in sources:
        if src.upper() in name_upper:
            return src
    return "Unknown"


def _extract_resolution(name: str) -> str:
    """Extract resolution from release name."""
    resolutions = ["2160p", "4K", "1080p", "1080i", "720p", "576p", "480p", "SD"]
    name_upper = name.upper()
    for res in resolutions:
        if res.upper() in name_upper:
            return res
    return "Unknown"


def _extract_format(name: str, path: Path) -> str:
    """Extract format from release name or file extension."""
    formats = ["FLAC", "MP3", "AAC", "OGG", "EPUB", "PDF", "MOBI", "AZW3", "CBR", "CBZ"]
    name_upper = name.upper()
    for fmt in formats:
        if fmt in name_upper:
            return fmt
    # Try file extension
    if path.is_file():
        ext = path.suffix.upper().lstrip(".")
        if ext in formats:
            return ext
    # Check first file in directory
    if path.is_dir():
        for f in path.rglob("*"):
            if f.is_file():
                ext = f.suffix.upper().lstrip(".")
                if ext in ["FLAC", "MP3", "EPUB", "PDF", "MOBI", "CBR", "CBZ"]:
                    return ext
                break
    return "Unknown"
