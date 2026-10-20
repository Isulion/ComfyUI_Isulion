"""Sandbox checks for IsulionLoadImagesNode directory resolution.

``folder_paths.get_input_directory`` is pointed at a temporary directory;
the node must refuse any path escaping it and force re-execution via NaN.
"""

import math
import os
import shutil
import sys
import tempfile
from unittest.mock import patch

from isulion_testkit import import_package

ESCAPING_PATHS = ["../..", "../../etc", "/abs/path", "sub/../../../outside"]


def _sandbox_setup():
    base = tempfile.mkdtemp(prefix="isulion-sandbox-")
    os.mkdir(os.path.join(base, "sub"))
    return base


def _patched_input_directory(base):
    folder_paths = sys.modules["folder_paths"]
    return patch.object(folder_paths, "get_input_directory", lambda: str(base))


def test_resolve_directory_keeps_relative_path_inside_sandbox():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionLoadImagesNode"]
    base = _sandbox_setup()
    try:
        with _patched_input_directory(base):
            resolved = cls._resolve_directory("sub")
        assert os.path.isdir(resolved)
        # The resolved path must live underneath the sandbox root.
        assert os.path.realpath(resolved).startswith(os.path.realpath(base) + os.sep)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def test_resolve_directory_rejects_escaping_paths():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionLoadImagesNode"]
    base = _sandbox_setup()
    try:
        with _patched_input_directory(base):
            for bad in ESCAPING_PATHS:
                try:
                    cls._resolve_directory(bad)
                except ValueError:
                    continue
                raise AssertionError(
                    f"_resolve_directory accepted sandbox escape: {bad!r}"
                )
    finally:
        shutil.rmtree(base, ignore_errors=True)


def test_is_changed_returns_nan_on_escape_attempt():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionLoadImagesNode"]
    base = _sandbox_setup()
    try:
        with _patched_input_directory(base):
            value = cls.IS_CHANGED(directory="../..")
        assert isinstance(value, float), type(value)
        assert math.isnan(value)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def test_is_changed_returns_stable_hash_for_valid_directory():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionLoadImagesNode"]
    base = _sandbox_setup()
    try:
        with open(os.path.join(base, "sub", "a.png"), "wb") as handle:
            handle.write(b"fake")
        with _patched_input_directory(base):
            first = cls.IS_CHANGED(directory="sub")
            second = cls.IS_CHANGED(directory="sub")
        assert isinstance(first, str) and len(first) == 40
        assert first == second
    finally:
        shutil.rmtree(base, ignore_errors=True)
