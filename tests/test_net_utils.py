"""Security checks for Core_Nodes/net_utils.py (loaded stand-alone).

No real network access happens: hosts are validated via literal IPs (numeric
lookups never hit DNS) and ``requests.get`` is replaced by a fake context
manager before exercising ``safe_download``.
"""

from unittest.mock import patch

from isulion_testkit import load_net_utils_directly

REJECTED_URLS = [
    # Disallowed schemes
    "ftp://example.com/file.zip",
    "file:///etc/passwd",
    "javascript:alert(1)",
    # Hostless URLs
    "http://",
    "https:///path/only",
    # Literal private / reserved IP targets (SSRF)
    "http://127.0.0.1/local.png",
    "http://10.1.2.3/internal.png",
    "http://192.168.0.42/router.png",
    "http://169.254.169.254/latest/meta-data/",
    "http://[::1]/local.png",
    # IPv4 smuggled inside IPv6 (mapped / NAT64) and non-global ranges
    "http://[::ffff:127.0.0.1]/local.png",
    "http://[::ffff:10.0.0.1]/internal.png",
    "http://[64:ff9b::7f00:1]/nat64.png",
    "http://203.0.113.5/documentation-range.png",
]

ACCEPTED_URL = "http://8.8.8.8/public.png"  # public literal IP, never fetched


def _expect_download_error(net_utils, url):
    try:
        net_utils.validate_url(url)
    except net_utils.DownloadError:
        return
    raise AssertionError(f"validate_url accepted a forbidden URL: {url!r}")


class _FakeRaw:
    def __init__(self, payload):
        self._payload = payload
        self.requested_size = None

    def read(self, size, decode_content=True):
        self.requested_size = size
        return self._payload[:size]


class _FakeResponse:
    def __init__(self, headers, payload):
        self.headers = headers
        self.raw = _FakeRaw(payload)
        self.closed = False
        self.is_redirect = "Location" in headers

    def close(self):
        self.closed = True

    def raise_for_status(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.closed = True
        return False


def _fake_get(headers=None, payload=b""):
    response = _FakeResponse(headers or {}, payload)

    def get(url, timeout=None, stream=False, allow_redirects=True):
        assert stream is True, "net_utils.safe_download must stream"
        assert allow_redirects is False, "redirects must be followed manually"
        return response

    get.response = response  # test-introspection handle
    return get


def test_validate_url_rejects_bad_schemes_hostless_and_private_ips():
    net_utils = load_net_utils_directly()
    for url in REJECTED_URLS:
        _expect_download_error(net_utils, url)


def test_validate_url_accepts_public_literal_ip():
    net_utils = load_net_utils_directly()
    net_utils.validate_url(ACCEPTED_URL)  # must not raise


def test_safe_download_tolerates_malformed_content_length_and_streams():
    net_utils = load_net_utils_directly()
    fake_get = _fake_get(headers={"Content-Length": "abc"}, payload=b"streamed-bytes")
    with patch.object(net_utils.requests, "get", fake_get):
        data = net_utils.safe_download(ACCEPTED_URL, timeout=1, max_bytes=1024)
    assert data == b"streamed-bytes"
    # It must still have attempted to stream up to cap+1 bytes.
    assert fake_get.response.raw.requested_size == 1024 + 1


def test_safe_download_rejects_when_content_length_exceeds_cap():
    net_utils = load_net_utils_directly()
    fake_get = _fake_get(headers={"Content-Length": str(4096)}, payload=b"")
    try:
        with patch.object(net_utils.requests, "get", fake_get):
            net_utils.safe_download(ACCEPTED_URL, timeout=1, max_bytes=1024)
    except net_utils.DownloadError:
        pass
    else:
        raise AssertionError("Content-Length above the cap must raise DownloadError")


def test_safe_download_rejects_body_larger_than_cap_while_streaming():
    net_utils = load_net_utils_directly()
    lying_header = {"Content-Length": "16"}  # header lies small...
    huge_body = b"x" * (2048 + 1)  # ...but streamed body exceeds the cap
    fake_get = _fake_get(headers=lying_header, payload=huge_body)
    try:
        with patch.object(net_utils.requests, "get", fake_get):
            net_utils.safe_download(ACCEPTED_URL, timeout=1, max_bytes=2048)
    except net_utils.DownloadError:
        pass
    else:
        raise AssertionError("Streamed body above the cap must raise DownloadError")


def test_safe_download_revalidates_redirect_targets():
    net_utils = load_net_utils_directly()
    hops = {
        ACCEPTED_URL: _FakeResponse({"Location": "http://169.254.169.254/latest/"}, b""),
    }
    requested = []

    def get(url, timeout=None, stream=False, allow_redirects=True):
        assert allow_redirects is False
        requested.append(url)
        return hops[url]

    try:
        with patch.object(net_utils.requests, "get", get):
            net_utils.safe_download(ACCEPTED_URL, timeout=1)
    except net_utils.DownloadError:
        pass
    else:
        raise AssertionError("a redirect to a private address must raise DownloadError")
    assert requested == [ACCEPTED_URL], "the private redirect target must never be fetched"


def test_safe_download_follows_public_redirects():
    net_utils = load_net_utils_directly()
    final_url = "http://1.1.1.1/final.png"
    hops = {
        ACCEPTED_URL: _FakeResponse({"Location": final_url}, b""),
        final_url: _FakeResponse({}, b"image-bytes"),
    }

    def get(url, timeout=None, stream=False, allow_redirects=True):
        return hops[url]

    with patch.object(net_utils.requests, "get", get):
        assert net_utils.safe_download(ACCEPTED_URL, timeout=1) == b"image-bytes"
    assert hops[ACCEPTED_URL].closed, "intermediate redirect responses must be closed"
