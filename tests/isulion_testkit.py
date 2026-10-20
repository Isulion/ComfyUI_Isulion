"""Shared infrastructure for the Isulion test suite.

The custom-node ecosystem assumes a full ComfyUI runtime (torch, numpy, PIL,
folder_paths). None of those are needed for the behaviour under test here, so
every one of them is replaced by a ``MagicMock`` before the package is
imported. Helpers are deliberately dependency-free (stdlib only) so the whole
suite runs under pytest *and* via the plain ``tests/run_all.py`` fallback.
"""

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

_PKG = None
_NET_UTILS = None


def stub_heavy_deps():
    """Install lightweight stand-ins for ComfyUI-only/heavy dependencies."""
    torch = MagicMock()
    torch.nn.functional = MagicMock()
    for name, module in [
        ("torch", torch),
        ("torch.nn", torch.nn),
        ("torch.nn.functional", torch.nn.functional),
        ("numpy", MagicMock()),
        ("PIL", MagicMock()),
        ("PIL.Image", MagicMock()),
        ("PIL.ImageOps", MagicMock()),
        ("requests", MagicMock()),
        ("folder_paths", MagicMock()),
    ]:
        sys.modules.setdefault(name, module)


def import_package():
    """Import the custom-node package (cached) with heavy deps stubbed."""
    global _PKG
    if _PKG is not None:
        return _PKG
    stub_heavy_deps()
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location(
        "isulion_pkg",
        str(ROOT / "__init__.py"),
        submodule_search_locations=[str(ROOT)],
    )
    pkg = importlib.util.module_from_spec(spec)
    sys.modules["isulion_pkg"] = pkg
    spec.loader.exec_module(pkg)
    _PKG = pkg
    return pkg


def load_net_utils_directly():
    """Load Core_Nodes/net_utils.py as a stand-alone module (cached)."""
    global _NET_UTILS
    if _NET_UTILS is not None:
        return _NET_UTILS
    stub_heavy_deps()
    spec = importlib.util.spec_from_file_location(
        "isulion_net_utils", str(ROOT / "Core_Nodes" / "net_utils.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["isulion_net_utils"] = module
    spec.loader.exec_module(module)
    _NET_UTILS = module
    return module


def load_fixture(name):
    """Return the parsed JSON fixture from tests/fixtures/."""
    with open(FIXTURES_DIR / name, "r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_json(value):
    """JSON-round-trip a value so tuples/lists compare equally."""
    return json.loads(json.dumps(value))
