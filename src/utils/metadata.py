"""Metadata extraction utilities (exiftool)."""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from src.utils.core import human_size, now_iso, validate_path_for_subprocess
from src.utils.media import (
    AUDIO_PRIORITY,
    _album_art_from_exif,
    _audio_props_from_ffprobe,
    _extract_album_art,
    _extract_video_thumbnail,
    _find_local_lyrics,
    _find_primary_file,
    _has_embedded_lyrics,
    extract_thumbnail,
)

logger = logging.getLogger(__name__)


def write_xml_metadata(
    release_name: str,
    media_type: str,
    path: Path,
    size_bytes: int,
    torrent_path: Path,
    nfo_path: Path,
    tags: str,
    out_dir: Path,
    metadata: dict | None = None,
    thumb_path: Path | None = None,
) -> Path:
    """Write XML sidecar file with upload metadata."""
    xml_path = out_dir / f"{release_name}.xml"
    metadata = metadata or {}

    root = ET.Element("tlt")
    ET.SubElement(root, "release_name").text = release_name
    ET.SubElement(root, "media_type").text = media_type
    ET.SubElement(root, "path").text = str(path)
    ET.SubElement(root, "size_bytes").text = str(size_bytes)
    ET.SubElement(root, "size_human").text = human_size(size_bytes)
    ET.SubElement(root, "torrent_path").text = str(torrent_path)
    ET.SubElement(root, "nfo_path").text = str(nfo_path)
    if thumb_path:
        ET.SubElement(root, "thumb_path").text = str(thumb_path)
    ET.SubElement(root, "tags").text = tags
    ET.SubElement(root, "created_at").text = now_iso()

    # Add extracted metadata
    if metadata:
        meta_elem = ET.SubElement(root, "metadata")
        for key, value in metadata.items():
            if value:
                ET.SubElement(meta_elem, key).text = str(value)

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    return xml_path


def extract_metadata(path: Path, media_type: str = "movies") -> dict:
    """Extract metadata from files using exiftool and NFO parsing.

    Returns dict with standardized keys based on media type:
    - movies/tv: title, year, description, imdb, tvmazeid, tvmazetype
    - music: artist, album, track, year, genre, format, bitrate, channels, source
    - books: title, author, publisher, year
    """
    if not shutil.which("exiftool"):
        logger.warning("exiftool not installed -- metadata extraction disabled")
        return {}

    target = _find_primary_file(path, media_type)
    result = {}

    # 1. Try NFO parsing first (often more reliable for IDs)
    if path.is_dir() or path.suffix.lower() == ".nfo":
        result.update(_extract_ids_from_nfos(path))

    if not target or not validate_path_for_subprocess(target):
        return result

    try:
        # Single exiftool call -- request all fields we need (including audio).
        exif_result = subprocess.run(
            ["exiftool", "-json", "-n", str(target)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if exif_result.returncode == 0:
            data = json.loads(exif_result.stdout)
            if data:
                raw = data[0]
                result.update(_normalize_metadata(raw, media_type))

                # Derive audio properties from the same exiftool output.
                if media_type == "music":
                    result.update(_audio_props_from_exif(raw))
                    if _has_embedded_lyrics(raw):
                        result["embedded_lyrics"] = True
                    art = _album_art_from_exif(raw)
                    if art:
                        result["album_art"] = art

        # Local lyrics lookup (sidecar .lrc/.txt) for music
        if media_type == "music" and path:
            lyrics = _find_local_lyrics(path)
            if lyrics:
                result["lyrics"] = lyrics
                result["lyrics_count"] = len(lyrics)

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError, json.JSONDecodeError):
        pass

    # ffprobe fallback / augmentation for music audio details
    if media_type == "music" and target:
        ffprobe_data = _audio_props_from_ffprobe(target)
        if ffprobe_data:
            for k, v in ffprobe_data.items():
                if not result.get(k):
                    result[k] = v

    return {k: v for k, v in result.items() if v}


def _audio_props_from_exif(raw: dict) -> dict:
    """Derive audio properties from an already-loaded exiftool dict.

    Avoids a second subprocess call -- reuses the full JSON output that
    extract_metadata() already fetched.
    """
    props: dict[str, str] = {
        "format": "MP3",
        "bitrate": "320",
        "channels": "2.0",
        "source": "WEB",  # Default assumption
    }

    try:
        ft = str(raw.get("FileType", "")).upper()
        props["format"] = ft if ft in ("FLAC", "MP3", "OGG", "OPUS", "M4A", "WAV") else "MP3"

        # Bitrate / quality
        if props["format"] == "FLAC":
            bits = raw.get("BitsPerSample", 16)
            props["bitrate"] = "24bit" if int(bits) > 16 else "16bit"
        else:
            br = raw.get("AudioBitrate", "320000")
            if isinstance(br, str):
                br = "".join(filter(str.isdigit, br))
            br_val = int(br) if br else 320000

            if br_val >= 320000:
                props["bitrate"] = "320"
            elif br_val >= 256000:
                props["bitrate"] = "V0"
            else:
                props["bitrate"] = "V2"

        # Channels
        ch = raw.get("Channels", 2)
        ch_val = int(ch)
        if ch_val == 1:
            props["channels"] = "1.0"
        elif ch_val == 2:
            props["channels"] = "2.0"
        elif ch_val == 6:
            props["channels"] = "5.1"
        elif ch_val == 8:
            props["channels"] = "7.1"
        else:
            props["channels"] = str(ch_val)

        # Sample rate
        sr = raw.get("SampleRate") or raw.get("AudioSampleRate")
        if sr:
            try:
                sr_val = float(sr)
                props["sample_rate"] = f"{sr_val / 1000:.1f} kHz" if sr_val >= 1000 else f"{sr_val:.0f} Hz"
            except (ValueError, TypeError):
                pass

        # Bit depth
        bits = raw.get("BitsPerSample") or raw.get("BitDepth")
        if bits:
            props["bit_depth"] = str(int(bits))

        # Encoder
        encoder = raw.get("Encoder") or raw.get("EncodedBy") or raw.get("Tool")
        if encoder:
            props["encoder"] = str(encoder)

        # Bitrate (kbps)
        br = raw.get("AudioBitrate") or raw.get("BitRate")
        if br:
            if isinstance(br, str):
                br = "".join(filter(str.isdigit, br))
            try:
                br_val = int(br)
                props["bitrate_kbps"] = f"{int(br_val / 1000)} kbps"
            except (ValueError, TypeError):
                pass
    except (ValueError, TypeError):
        pass

    return props


def _extract_ids_from_nfos(path: Path) -> dict:
    """Scan directory for .nfo files and extract IMDB/TVMaze IDs."""
    ids = {}
    nfo_files = []
    if path.is_file() and path.suffix.lower() == ".nfo":
        nfo_files.append(path)
    elif path.is_dir():
        nfo_files.extend(list(path.glob("*.nfo")) + list(path.glob("*.NFO")))

    imdb_pattern = re.compile(r"tt\d{7,9}")
    tvmaze_pattern = re.compile(r"tvmaze\.com/shows/(\d+)")

    for nfo in nfo_files:
        try:
            content = nfo.read_text(errors="ignore")
            # IMDB
            imdb_match = imdb_pattern.search(content)
            if imdb_match and not ids.get("imdb"):
                ids["imdb"] = imdb_match.group(0)

            # TVMaze
            tvmaze_match = tvmaze_pattern.search(content)
            if tvmaze_match and not ids.get("tvmazeid"):
                ids["tvmazeid"] = tvmaze_match.group(1)
        except Exception:
            continue
    return ids


def _normalize_metadata(raw: dict, media_type: str) -> dict:
    """Normalize exiftool output to standard keys."""
    result = {}

    if media_type in ("movies", "tv"):
        result["title"] = raw.get("Title") or raw.get("MovieName") or ""
        result["year"] = raw.get("Year") or raw.get("ContentCreateDate", "")[:4] if raw.get("ContentCreateDate") else ""
        result["description"] = raw.get("Description") or raw.get("Comment") or ""

        # ID Extraction from tags
        result["imdb"] = raw.get("IMDB") or raw.get("IMDB_ID") or ""
        result["tvmazeid"] = raw.get("TVMAZE_ID") or raw.get("TVMazeID") or ""

        # TV specific
        if media_type == "tv":
            result["show"] = raw.get("TVShow") or raw.get("Album") or ""
            result["season"] = raw.get("TVSeason") or raw.get("SeasonNumber") or ""
            result["episode"] = raw.get("TVEpisode") or raw.get("EpisodeNumber") or ""

    elif media_type == "music":
        result["artist"] = raw.get("Artist") or raw.get("AlbumArtist") or ""
        result["album_artist"] = raw.get("AlbumArtist") or raw.get("Band") or ""
        result["album"] = raw.get("Album") or ""
        result["track"] = raw.get("Title") or raw.get("Track") or ""
        result["year"] = str(raw.get("Year") or "")
        result["genre"] = raw.get("Genre") or ""
        result["track_number"] = raw.get("TrackNumber") or ""
        result["track_total"] = raw.get("TrackCount") or raw.get("TrackTotal") or ""
        result["disc_number"] = raw.get("DiscNumber") or raw.get("Disc") or ""
        result["disc_total"] = raw.get("DiscCount") or raw.get("DiscTotal") or ""
        result["label"] = raw.get("RecordLabel") or raw.get("Label") or raw.get("Publisher") or ""
        result["catalog"] = raw.get("CatalogNumber") or raw.get("CatalogNo") or ""
        result["isrc"] = raw.get("ISRC") or raw.get("ISRCCode") or ""
        result["composer"] = raw.get("Composer") or ""

    elif media_type == "books":
        result["title"] = raw.get("Title") or ""
        result["author"] = raw.get("Author") or raw.get("Creator") or ""
        result["publisher"] = raw.get("Publisher") or ""
        result["year"] = str(raw.get("CreateDate", ""))[:4] if raw.get("CreateDate") else ""
        result["isbn"] = raw.get("ISBN") or ""

    # Clean empty strings
    return {k: v for k, v in result.items() if v}
