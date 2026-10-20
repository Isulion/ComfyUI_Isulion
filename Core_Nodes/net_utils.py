"""Shared, hardened download helper for URL-fetching nodes.

URLs are validated before any network call: only http(s) schemes are
allowed and hostnames resolving to private/reserved networks (SSRF
guards) are rejected outright.
"""

import logging
import socket
from ipaddress import ip_address, ip_network
from urllib.parse import urljoin, urlparse

import requests

logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB safety cap (decompression-bomb guard)
MAX_REDIRECTS = 5

_BLOCKED_NETS = tuple(ip_network(n) for n in (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
    "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.168.0.0/16",
    "198.18.0.0/15", "224.0.0.0/3", "::/128", "::1/128", "fc00::/7", "fe80::/10",
    "64:ff9b::/96", "64:ff9b:1::/48",  # NAT64 prefixes can embed private IPv4
))


class DownloadError(Exception):
    """Raised when a URL fails scheme/host validation or exceeds size limits."""


def _assert_public_host(host: str) -> None:
    """Resolve `host` once and reject any private/reserved resolved address."""
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, OSError, UnicodeError):
        raise DownloadError(f"Could not resolve host {host!r}")
    for info in infos:
        addr = info[4][0]
        try:
            ip = ip_address(addr.split("%", 1)[0])
        except ValueError:
            continue
        # Unwrap IPv4-mapped addresses (::ffff:a.b.c.d) so
        # e.g. [::ffff:127.0.0.1] is judged as 127.0.0.1.
        if ip.version == 6 and ip.ipv4_mapped is not None:
            ip = ip.ipv4_mapped
        if (not ip.is_global or ip.is_multicast
                or any(ip in net for net in _BLOCKED_NETS)):
            raise DownloadError(
                f"Host {host!r} resolves to a blocked (private/reserved) address: {ip}"
            )


def validate_url(url: str) -> None:
    """Reject non-http(s), hostless URLs and private-network targets."""
    parsed = urlparse(str(url))
    if parsed.scheme not in ("http", "https"):
        raise DownloadError(f"URL scheme not allowed: {parsed.scheme!r}")
    if not parsed.netloc:
        raise DownloadError("URL has no host")
    host = parsed.hostname
    if host:
        _assert_public_host(host)


def _open_validated(url: str, timeout: int):
    """GET `url`, following redirects manually so every hop is re-validated."""
    for _ in range(MAX_REDIRECTS + 1):
        validate_url(url)
        response = requests.get(url, timeout=timeout, stream=True, allow_redirects=False)
        if not response.is_redirect:
            return response
        location = response.headers.get("Location", "")
        response.close()
        url = urljoin(url, location)
    raise DownloadError(f"Too many redirects (> {MAX_REDIRECTS})")


def safe_download(url: str, timeout: int = 15, max_bytes: int = MAX_IMAGE_BYTES) -> bytes:
    """Download `url` enforcing http(s)-only schemes, public-host checks on every
    redirect hop, and a hard size cap.

    Residual risk: the hostname is resolved once for validation and again by
    `requests`, so a DNS-rebinding host could still swap addresses in between.
    """
    with _open_validated(url, timeout) as response:
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        length = None
        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                logger.warning("Malformed Content-Length header ignored: %r", content_length)
        if length is not None and length > max_bytes:
            raise DownloadError(f"Content too large ({content_length} bytes > {max_bytes})")
        data = response.raw.read(max_bytes + 1, decode_content=True)
    if len(data) > max_bytes:
        raise DownloadError(f"Content exceeded {max_bytes} bytes while streaming")
    return data
