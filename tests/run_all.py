#!/usr/bin/env python3
"""Fallback sequential test runner (used when pytest is unavailable).

Runs every ``test_*`` function of the suite with a minimal assert harness,
prints a PASS/FAIL summary, and exits non-zero on any failure. It is harmless
to run alongside pytest and is the required entry point on machines where
pytest cannot be installed:

    python3 tests/run_all.py
"""

import importlib
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import isulion_testkit  # noqa: E402

MODULES = [
    "test_registration",
    "test_node_contracts",
    "test_theme_registry",
    "test_selectors",
    "test_net_utils",
    "test_civitai_shapes",
    "test_load_images_sandbox",
    "test_censored_part",
    "test_prompt_vault",
    "test_space_invaders",
]


def main() -> int:
    isulion_testkit.stub_heavy_deps()

    passed = 0
    failures = []

    for module_name in MODULES:
        module = importlib.import_module(module_name)
        tests = sorted(
            (name, obj) for name, obj in vars(module).items()
            if name.startswith("test_") and callable(obj)
        )
        print(f"=== {module_name}: {len(tests)} tests ===")
        for name, func in tests:
            label = f"{module_name}.{name}"
            try:
                func()
            except Exception:
                failures.append((label, traceback.format_exc()))
                print(f"  FAIL {name}")
            else:
                passed += 1
                print(f"  PASS {name}")
        print()

    total = passed + len(failures)
    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} passed, {len(failures)} failed")
    for label, tb in failures:
        print("-" * 60)
        print(f"FAILED: {label}\n{tb}")
    print("=" * 60)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
