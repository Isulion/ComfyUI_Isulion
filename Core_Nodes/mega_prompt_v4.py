"""
Isulion Mega Prompt V4 « Prompt Jackpot ».

Python side of web/mega_prompt_v4.js: the browser edits a versioned JSON state
(hidden ``machine_state`` widget); this module parses it, rolls the unlocked
reels with the V3 theme handlers and assembles the prompt. The same ``roll``
serves workflow execution and the preview routes (mega_prompt_v4_routes.py).
"""

import json
import logging

from .mega_prompt_V3 import get_theme_registry

logger = logging.getLogger(__name__)

STATE_VERSION = 1
DEFAULT_STATE = '{"version": 1}'
REEL_NAMES = ("theme", "subject", "location", "style", "effects")
COMPLEXITIES = ("simple", "detailed", "complex")

# Which optional keys each reel carries in the state
_REEL_FIELDS = {
    "subject": ("custom",),
    "location": ("custom", "enabled"),
    "style": ("enabled",),
    "effects": ("enabled",),
}


def default_state():
    reels = {}
    for name, extra in _REEL_FIELDS.items():
        reel = {"text": "", "locked": False}
        if "custom" in extra:
            reel["custom"] = ""
        if "enabled" in extra:
            reel["enabled"] = True
        reels[name] = reel
    return {
        "version": STATE_VERSION,
        "theme": {"name": "", "locked": False},
        "reels": reels,
        "complexity": "detailed",
        "lora": "",
        "frozen_prompt": "",
    }


def _str(value):
    return value if isinstance(value, str) else ""


def _bool(value, default):
    # strict: 1/"yes" are not booleans
    return value if isinstance(value, bool) else default


def _dict(value):
    return value if isinstance(value, dict) else {}


def parse_state(raw):
    """Return a complete, fresh v1 state; anything invalid falls back to defaults."""
    data = raw
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except ValueError:
            data = None
    state = default_state()
    if not isinstance(data, dict) or data.get("version") != STATE_VERSION or isinstance(data.get("version"), bool):
        return state

    theme = _dict(data.get("theme"))
    state["theme"] = {"name": _str(theme.get("name")), "locked": _bool(theme.get("locked"), False)}

    reels_in = _dict(data.get("reels"))
    for name, reel in state["reels"].items():
        src = _dict(reels_in.get(name))
        reel["text"] = _str(src.get("text"))
        reel["locked"] = _bool(src.get("locked"), False)
        if "custom" in reel:
            reel["custom"] = _str(src.get("custom"))
        if "enabled" in reel:
            reel["enabled"] = _bool(src.get("enabled"), True)

    complexity = data.get("complexity")
    state["complexity"] = complexity if complexity in COMPLEXITIES else "detailed"
    state["lora"] = _str(data.get("lora"))
    state["frozen_prompt"] = _str(data.get("frozen_prompt"))
    return state


COMPLEXITY_SUFFIX = {
    "simple": "",
    "detailed": "highly detailed, sharp focus",
    "complex": "highly detailed, intricate textures, cinematic composition, dramatic lighting, masterpiece",
}
# Generic quality boilerplate removed from each component in SIMPLE mode
SIMPLE_DROP = frozenset({
    "masterpiece", "best quality", "highly detailed", "ultra detailed", "artistic excellence",
    "professional quality", "8k", "4k", "8k resolution",
})


def simplify_component(text):
    kept = [chunk.strip() for chunk in text.split(",")
            if chunk.strip() and chunk.strip().strip("()").strip().lower() not in SIMPLE_DROP]
    return ", ".join(kept)


def assemble_prompt(state):
    """Return (prompt, segments); segments carry the reel each piece came from."""
    frozen = state["frozen_prompt"]
    if frozen.strip():
        return frozen, [{"reel": "frozen", "text": frozen}]

    simple = state["complexity"] == "simple"
    segments = []
    for name, reel in state["reels"].items():
        if not reel.get("enabled", True):
            continue
        text = simplify_component(reel["text"]) if simple else reel["text"].strip()
        if text:
            segments.append({"reel": name, "text": text})
    suffix = COMPLEXITY_SUFFIX[state["complexity"]]
    if suffix:
        segments.append({"reel": "complexity", "text": suffix})
    lora = state["lora"].strip()
    if lora:
        segments.append({"reel": "lora", "text": lora})

    seen, unique = set(), []
    for seg in segments:
        key = seg["text"].strip().lower()
        if key not in seen:
            seen.add(key)
            unique.append(seg)
    return ", ".join(seg["text"] for seg in unique), unique


def theme_entry(name, registry=None):
    registry = registry or get_theme_registry()
    handler = registry.handlers.get(name)
    if handler is None:
        return {"name": name, "display": name, "icon": "🎰", "label": name}
    display = getattr(handler, "DISPLAY_NAME", "") or name
    icon, _, label = display.partition(" ")
    if not label:
        icon, label = "🎰", display
    return {"name": name, "display": display, "icon": icon, "label": label}


def list_themes(registry=None):
    """Every registered theme (no "random" pseudo-theme), sorted like the V3 dropdown."""
    registry = registry or get_theme_registry()
    entries = [theme_entry(name, registry) for name in registry.handlers]
    return sorted(entries, key=lambda e: e["display"].split(" ", 1)[-1].strip())
