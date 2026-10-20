"""Runs the Node harness for web/mega_prompt_v4.js (skipped when node is not installed)."""

import shutil
import subprocess

from isulion_testkit import ROOT


def test_js_extension_syntax_and_harness():
    node = shutil.which("node")
    if node is None:
        print("[skip] node not installed")
        return
    for name in ("mega_prompt_v4.js", "mega_prompt_v4_core.js"):
        path = ROOT / "web" / name
        if path.exists():
            subprocess.run([node, "--check", str(path)], check=True)
    subprocess.run([node, "tests/js/test_mega_prompt_v4.mjs"], check=True, timeout=120, cwd=ROOT,
                   stdout=subprocess.DEVNULL)
