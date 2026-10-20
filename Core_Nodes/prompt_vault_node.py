"""Prompt Vault nodes: a shared JSON-backed library of named prompt fragments.

Two nodes share one vault file. By default it lives in ComfyUI's user
directory (user/isulion/prompt_vault.json), outside this git checkout, so
saving entries never blocks `git pull` / ComfyUI-Manager updates. Until the
first save, the bundled prompt_vault.example.json entries are offered.

- IsulionPromptVaultSave: stores/updates an entry under a name and passes the
  text through unchanged, so it can be chained straight into KSampler.
- IsulionPromptVaultLoad: exposes every stored entry as a dropdown.

The vault path can be overridden with the ISULION_PROMPT_VAULT environment
variable. The variable is read on every call (no caching) so tests and
runtime overrides both work without re-importing.
"""

import json
import logging
import os
import tempfile
import threading

logger = logging.getLogger(__name__)

MAX_NAME_LENGTH = 64
_LOCK = threading.Lock()


_EXAMPLE_VAULT = os.path.join(os.path.dirname(__file__), "prompt_vault.example.json")


def _default_vault_path():
    try:
        import folder_paths
        user_dir = folder_paths.get_user_directory()
    except (ImportError, AttributeError):
        user_dir = None
    if not isinstance(user_dir, str):
        # Outside ComfyUI: fall back to a gitignored folder inside the package.
        user_dir = os.path.join(os.path.dirname(__file__), "user_data")
    return os.path.join(user_dir, "isulion", "prompt_vault.json")


def _vault_path():
    override = os.environ.get("ISULION_PROMPT_VAULT")
    return override if override else _default_vault_path()


def _empty_vault():
    return {"version": 1, "entries": []}


def _read_vault(path):
    """Return the parsed vault; missing/corrupt files degrade to an empty vault.

    A missing *default* vault is seeded from the bundled example entries.
    """
    if not os.path.exists(path):
        if path == _default_vault_path() and os.path.exists(_EXAMPLE_VAULT):
            return _read_vault(_EXAMPLE_VAULT)
        return _empty_vault()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        logger.warning("PromptVault - could not read %s (%s); treating as empty", path, exc)
        return _empty_vault()
    if not isinstance(data, dict):
        logger.warning("PromptVault - vault root is not an object in %s; treating as empty", path)
        return _empty_vault()
    entries = data.get("entries")
    if not isinstance(entries, list):
        logger.warning("PromptVault - 'entries' missing or not a list in %s; treating as empty", path)
        return {"version": data.get("version", 1), "entries": []}
    clean = [
        entry for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("name"), str) and isinstance(entry.get("text"), str)
    ]
    return {"version": data.get("version", 1), "entries": clean}


def _write_vault(path, data):
    """Atomically write the vault (temp file + os.replace)."""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".prompt_vault_", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        # mkstemp creates 0600 files; keep the vault readable like a normal file.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


def _sanitize_name(raw):
    """Collapse whitespace runs and cap the length so names stay dropdown-friendly."""
    return " ".join(str(raw).split())[:MAX_NAME_LENGTH].strip()


def vault_names(path=None):
    """Names of all vault entries, in stored order."""
    return [entry["name"] for entry in _read_vault(path or _vault_path())["entries"]]


class IsulionPromptVaultSave:
    """Store a prompt fragment in the vault under a name (upsert)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {"default": "", "placeholder": "entry name"}),
                "text": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "save"
    CATEGORY = "Isulion/Utilities"

    def save(self, name, text):
        clean_name = _sanitize_name(name)
        if not clean_name:
            raise ValueError("PromptVault - 'name' is empty; give the entry a name before saving.")
        with _LOCK:
            path = _vault_path()
            vault = _read_vault(path)
            entries = vault["entries"]
            for index, entry in enumerate(entries):
                if entry["name"] == clean_name:
                    entries[index] = {"name": clean_name, "text": text}
                    break
            else:
                entries.append({"name": clean_name, "text": text})
            _write_vault(path, {"version": 1, "entries": entries})
        logger.info("PromptVault - saved entry '%s' (%d chars)", clean_name, len(text))
        return (text,)


class IsulionPromptVaultLoad:
    """Fetch a stored prompt fragment by name."""

    @classmethod
    def INPUT_TYPES(cls):
        names = vault_names() or [""]
        return {
            "required": {
                # allowCustomValue: the combo is built at page load, but users can
                # type any name directly (e.g. one saved moments ago) without a refresh.
                "entry": (names, {"default": names[0], "allowCustomValue": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load"
    CATEGORY = "Isulion/Utilities"

    @classmethod
    def IS_CHANGED(cls, entry):
        # Re-run whenever the vault file changes, otherwise ComfyUI's cache
        # would keep returning the text from before the last save.
        try:
            return os.stat(_vault_path()).st_mtime_ns
        except OSError:
            return float("nan")

    @classmethod
    def VALIDATE_INPUTS(cls, entry):
        # Accept names that are not in the dropdown yet (e.g. saved earlier in
        # the same run); load() reports unknown names at execution time.
        return True

    def load(self, entry):
        entries = _read_vault(_vault_path())["entries"]
        for item in entries:
            if item["name"] == entry:
                return (item["text"],)
        available = ", ".join(item["name"] for item in entries) or "(none)"
        raise ValueError(f"PromptVault - unknown entry '{entry}'. Available: {available}")
