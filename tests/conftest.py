"""Pytest bootstrap for the Isulion test suite.

This file lives in tests/ (NOT at the repo root) on purpose: the repo root is
itself an importable package (``__init__.py``), so a root conftest.py would be
imported *through* that package and would trigger ``import torch`` before any
stubbing could happen.

Stubs the ComfyUI-only / heavy third-party modules (torch, numpy, PIL,
requests, folder_paths) BEFORE pytest collects any test module, then exposes
the shared helpers from tests/isulion_testkit.py.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent
for entry in (str(TESTS_DIR), str(ROOT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from isulion_testkit import stub_heavy_deps  # noqa: E402

stub_heavy_deps()
