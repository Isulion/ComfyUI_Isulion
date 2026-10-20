"""Behaviour tests for the Prompt Vault save/load nodes.

Every test that touches the vault redirects it to a temp file via the
ISULION_PROMPT_VAULT environment variable (or a temp default path), so neither
the bundled example vault nor the user's real vault is touched by the suite.
"""

import contextlib
import json
import os
import sys
import tempfile

from isulion_testkit import ROOT, import_package


@contextlib.contextmanager
def _env_vault(path):
    """Point ISULION_PROMPT_VAULT at `path` for the duration of the block."""
    old = os.environ.get("ISULION_PROMPT_VAULT")
    os.environ["ISULION_PROMPT_VAULT"] = str(path)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("ISULION_PROMPT_VAULT", None)
        else:
            os.environ["ISULION_PROMPT_VAULT"] = old


@contextlib.contextmanager
def _clear_vault_env():
    """Ensure ISULION_PROMPT_VAULT is unset (bundled default vault in use)."""
    old = os.environ.get("ISULION_PROMPT_VAULT")
    os.environ.pop("ISULION_PROMPT_VAULT", None)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("ISULION_PROMPT_VAULT", None)
        else:
            os.environ["ISULION_PROMPT_VAULT"] = old


def _nodes():
    pkg = import_package()
    save_cls = pkg.NODE_CLASS_MAPPINGS["IsulionPromptVaultSave"]
    load_cls = pkg.NODE_CLASS_MAPPINGS["IsulionPromptVaultLoad"]
    return save_cls(), load_cls()


def _read_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def test_save_then_load_roundtrip():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            assert saver.save("hero", "a neon hero") == ("a neon hero",)
            data = _read_file(vault_path)
            assert data["version"] == 1
            assert data["entries"] == [{"name": "hero", "text": "a neon hero"}]
            assert loader.load("hero") == ("a neon hero",)


def test_save_upserts_in_place_without_duplicates():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            saver.save("a", "first a")
            saver.save("b", "first b")
            saver.save("a", "second a")

            data = _read_file(vault_path)
            names = [entry["name"] for entry in data["entries"]]
            assert names == ["a", "b"], "upsert must keep the original order"
            texts = {entry["name"]: entry["text"] for entry in data["entries"]}
            assert texts == {"a": "second a", "b": "first b"}
            assert loader.load("a") == ("second a",)


def test_name_sanitization_collapses_whitespace_and_caps_length():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            saver.save("  my   hero ", "text one")
            data = _read_file(vault_path)
            assert [entry["name"] for entry in data["entries"]] == ["my hero"]
            assert loader.load("my hero") == ("text one",)

            long_name = "x" * 100
            saver.save(long_name, "long name text")
            data = _read_file(vault_path)
            names = [entry["name"] for entry in data["entries"]]
            assert len(names) == 2
            assert names[1] == "x" * 64


def test_empty_name_raises_value_error():
    saver, _ = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            for bad_name in ("", "   ", "\t\n"):
                try:
                    saver.save(bad_name, "text")
                except ValueError:
                    pass
                else:
                    raise AssertionError(f"save({bad_name!r}) must raise ValueError")
        assert not os.path.exists(vault_path), "failed saves must not create the file"


def test_load_missing_entry_raises_with_available_names():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            saver.save("hero", "text")
            try:
                loader.load("nope")
            except ValueError as exc:
                assert "hero" in str(exc)
                assert "nope" in str(exc)
            else:
                raise AssertionError("load('nope') must raise ValueError")


def test_corrupt_vault_degrades_to_empty_and_save_recovers():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            with open(vault_path, "w", encoding="utf-8") as handle:
                handle.write("not json {{{")

            contract = loader.INPUT_TYPES()
            assert contract["required"]["entry"][0] == [""], (
                "corrupt vault must degrade to an empty dropdown"
            )

            saver.save("recovered", "text")
            data = _read_file(vault_path)
            assert data["entries"] == [{"name": "recovered", "text": "text"}]


def test_missing_vault_file_is_treated_as_empty():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "does_not_exist", "vault.json")
        with _env_vault(vault_path):
            contract = loader.INPUT_TYPES()
            assert contract["required"]["entry"][0] == [""]
            assert contract["required"]["entry"][1]["default"] == ""

            try:
                loader.load("")
            except ValueError as exc:
                assert "(none)" in str(exc)
            else:
                raise AssertionError("load('') on an empty vault must raise ValueError")

            saver.save("first", "text")
            assert os.path.exists(vault_path), "save must create the missing file"


def test_bundled_default_vault_has_example_entries():
    loader = _nodes()[1]
    vault_module = sys.modules[type(loader).__module__]
    original_default = vault_module._default_vault_path
    tmp = tempfile.TemporaryDirectory()
    vault_module._default_vault_path = lambda: os.path.join(tmp.name, "isulion", "prompt_vault.json")
    try:
        with _clear_vault_env():
            _check_bundled_examples(loader)
    finally:
        vault_module._default_vault_path = original_default
        tmp.cleanup()


def _check_bundled_examples(loader):
    """A missing default vault must expose the bundled example entries."""
    bundled = ROOT / "Core_Nodes" / "prompt_vault.example.json"
    data = json.loads(bundled.read_text(encoding="utf-8"))
    assert data["version"] == 1
    entries = data["entries"]
    assert len(entries) == 3, "bundled vault must ship exactly 3 example entries"
    names = [entry["name"] for entry in entries]
    assert len(set(names)) == 3
    assert all(entry["text"].strip() for entry in entries)

    contract = loader.INPUT_TYPES()
    assert contract["required"]["entry"][0] == names, (
        "dropdown must mirror the bundled vault order"
    )
    assert contract["required"]["entry"][1]["default"] == names[0]


def test_load_reruns_when_vault_changes_and_accepts_unlisted_names():
    saver, loader = _nodes()
    with tempfile.TemporaryDirectory() as tmp:
        vault_path = os.path.join(tmp, "vault.json")
        with _env_vault(vault_path):
            saver.save("hero", "A")
            before = type(loader).IS_CHANGED("hero")
            os.utime(vault_path, ns=(1, 1))  # force a distinct mtime on fast filesystems
            saver.save("hero", "B")
            assert type(loader).IS_CHANGED("hero") != before, (
                "IS_CHANGED must change after a save, or ComfyUI serves stale text"
            )
            assert loader.load("hero") == ("B",)
            assert type(loader).VALIDATE_INPUTS("not-in-dropdown-yet") is True
