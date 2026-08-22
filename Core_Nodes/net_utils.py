"""Shared, hardened download helper for URL-fetching nodes."""

import logging
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB safety cap (decompression-bomb guard)


class DownloadError(Exception):
    """Raised when a URL fails scheme validation or exceeds size limits."""


def validate_url(url: str) -> None:
    """Reject non-http(s) or hostless URLs before any network call."""
    parsed = urlparse(str(url))
    if parsed.scheme not in ("http", "https"):
        raise DownloadError(f"URL scheme not allowed: {parsed.scheme!r}")
    if not parsed.netloc:
        raise DownloadError("URL has no host")


def safe_download(url: str, timeout: int = 15, max_bytes: int = MAX_IMAGE_BYTES) -> bytes:
    """Download `url` enforcing http(s)-only schemes and a hard size cap."""
    validate_url(url)
    with requests.get(url, timeout=timeout, stream=True) as response:
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        if content_length is not None and int(content_length) > max_bytes:
            raise DownloadError(f"Content too large ({content_length} bytes > {max_bytes})")
        data = response.raw.read(max_bytes + 1, decode_content=True)
    if len(data) > max_bytes:
        raise DownloadError(f"Content exceeded {max_bytes} bytes while streaming")
    return data
