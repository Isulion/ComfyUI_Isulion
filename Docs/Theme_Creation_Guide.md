# Theme Creation Guide

This guide documents how to add a new theme to both the **IsulionMegaPromptV3** (single theme) and **Isulion Multiple Prompt Generator** nodes.

## Architecture Overview

```
Core_Nodes/
├── mega_prompt_V3.py               # Node (reads themes from the handler registry)
├── mega_prompt_all_themes.py        # Multiple Prompt Generator (theme categories)
├── configs/
│   └── <theme>_config.json          # Data lists (characters, locations, styles, effects...)
└── theme_handlers/
    ├── __init__.py                  # Package init
    ├── registry.py                  # @register_theme decorator (THEME_HANDLERS registry)
    ├── base_handler.py              # BaseThemeHandler (abstract)
    └── <theme>_handler.py           # Handler logic (auto-discovered & registered)
```

## Step-by-step: Add theme `my_theme`

You only need to create **2 files** and add one line to a third for the Multiple Prompt Generator. Nothing else needs to be registered — auto-discovery handles the rest.

---

### 1. Create the JSON config file

**File:** `Core_Nodes/configs/my_theme_config.json`

The top-level key **must match the internal name** (snake_case).

```json
{
    "my_theme": {
        "characters": ["knight", "wizard", "dragon"],
        "outfits": ["plate armor", "robe", "scales"],
        "poses": ["battle stance", "casting spell"],
        "expressions": ["determined", "mysterious"],
        "locations": ["castle", "enchanted forest"],
        "styles": ["gothic", "medieval fantasy"],
        "effects": ["magic aura", "dragon fire"],
        "lighting": ["dramatic sunset", "torchlight"],
        "times": ["golden hour", "midnight"],
        "weather": ["clear sky", "misty"],
        "moods": ["epic", "whimsical"]
    }
}
```

Any category keys work — the handler reads them with dot notation: `"my_theme.characters"`.

---

### 2. Create the handler class

**File:** `Core_Nodes/theme_handlers/my_theme_handler.py`

Inherit `BaseThemeHandler`, decorate the class with `@register_theme("my_theme")`, and set a `DISPLAY_NAME` attribute (emoji + title, exactly as it should appear in the ComfyUI dropdown). Implement `generate()`, using `self._get_random_choice("my_theme.<key>")` to pull from your config.

```python
from typing import Dict
from .base_handler import BaseThemeHandler
from .registry import register_theme


@register_theme("my_theme")
class MyThemeHandler(BaseThemeHandler):
    """Handler for My Theme."""

    DISPLAY_NAME = "⚔️ My Theme"

    def generate(
        self,
        custom_subject: str = "",
        custom_location: str = "",
        include_environment: bool = True,
        include_style: bool = True,
        include_effects: bool = True,
    ) -> Dict[str, str]:
        components = {}

        character = self._get_random_choice("my_theme.characters")
        outfit = self._get_random_choice("my_theme.outfits")
        pose = self._get_random_choice("my_theme.poses")
        expression = self._get_random_choice("my_theme.expressions")

        if custom_subject:
            components["subject"] = (
                f"((masterful {character} rendition)) of {custom_subject}, "
                f"((wearing {outfit})), ((in {pose})), "
                f"((with {expression} expression))"
            )
        else:
            components["subject"] = (
                f"((masterful {character})) wearing ((detailed {outfit})), "
                f"((in {pose})), ((with {expression} expression))"
            )

        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((beautiful {custom_location})), "
                    f"((detailed environment))"
                )
            else:
                location = self._get_random_choice("my_theme.locations")
                time = self._get_random_choice("my_theme.times")
                weather = self._get_random_choice("my_theme.weather")
                components["environment"] = (
                    f"in ((stunning {location})) during (({time})) "
                    f"with (({weather}))"
                )

        if include_style:
            style = self._get_random_choice("my_theme.styles")
            components["style"] = (
                f"((masterfully rendered in {style} style)), "
                f"((professional composition)), 8k resolution"
            )

        if include_effects:
            effect = self._get_random_choice("my_theme.effects")
            mood = self._get_random_choice("my_theme.moods")
            lighting = self._get_random_choice("my_theme.lighting")
            components["effects"] = (
                f"with (({effect})), (({mood} atmosphere)), "
                f"((beautiful {lighting}))"
            )

        return components
```

**Contract:** `generate()` must return a `Dict[str, str]` with keys `subject`, `environment`, `style`, `effects`.

---

### 3. Done — nothing else to register

The `@register_theme("my_theme")` decorator adds your handler to the central registry (`theme_handlers/registry.py`) as soon as the module is loaded. Auto-discovery picks up new handler files automatically:

- **No edits to `theme_handlers/__init__.py`**
- **No edits to `mega_prompt_V3.py`** (no handler-name map or emoji-mapping edits)

Your theme appears in the IsulionMegaPromptV3 dropdown under its `DISPLAY_NAME`, linked to the internal name you registered.

---

### 4. Add to Isulion Multiple Prompt Generator

**File:** `Core_Nodes/mega_prompt_all_themes.py`

Add your display name to **exactly one** category in `theme_categories`. A theme left out of every category cannot be generated by the Multiple Prompt Generator, not even in "All Themes" mode:

```python
theme_categories = {
    # ...
    "Science Fiction & Fantasy": [
        # ...
        "⚔️ My Theme",    # <-- add here
        # ...
    ],
    # ...
}
```

The node automatically picks it up from there. If your theme doesn't fit an existing category, you can create a new one.

---

## Summary checklist

| # | File | Action |
|---|------|--------|
| 1 | `Core_Nodes/configs/my_theme_config.json` | Create JSON with data lists |
| 2 | `Core_Nodes/theme_handlers/my_theme_handler.py` | Create handler class with `@register_theme("my_theme")` + `DISPLAY_NAME` |
| 3 | `Core_Nodes/mega_prompt_all_themes.py` | Add the display name to one `theme_categories` list |

After making these changes, **restart ComfyUI**.

## How the config manager loads data

`ConfigManager` (`Core_Nodes/configs/config_manager.py`) reads **all** `*.json` files from `Core_Nodes/configs/` on startup, in alphabetical order, and merges them into a single `self.configs` dict. Top-level keys must be unique across files: a duplicate overrides the earlier file and logs a warning. The top-level key of each JSON file becomes the lookup key. Your config file can be named anything — `my_theme_config.json` — as long as its top-level key matches the internal name.

A handler calls `self._get_random_choice("my_theme.characters")` which resolves to `self.config.get_config("my_theme.characters")` → `self.configs["my_theme"]["characters"]`.

## Naming conventions

| What | Convention | Example |
|------|-----------|---------|
| Internal name | `snake_case` | `my_theme` |
| Handler class | `PascalCase` + `ThemeHandler` suffix | `MyThemeHandler` |
| Config file | `snake_case_config.json` | `my_theme_config.json` |
| Display name | Emoji + Title Case | `⚔️ My Theme` |
| Config JSON key | Same as internal name | `"my_theme": { ... }` |
| Handler filename | `snake_case_handler.py` | `my_theme_handler.py` |

## Available helper methods on `BaseThemeHandler`

| Method | Purpose |
|--------|---------|
| `_get_random_choice(key)` | Pick one random item from the config list at `"theme.key"` |
| `_get_safe_random_choice(key, default)` | Same but returns `default` if not found |
| `_get_random_choices(key, count)` | Pick `count` random items (with repeats if needed) |

## Troubleshooting

- **"Duplicate theme registration"** → another handler is already registered under your internal name; pick a unique one
- **"Handler not found" / handler never loads** → verify the module is importable (no syntax errors) and that `@register_theme("my_theme")` uses the same internal name as your config JSON top-level key
- **"Config key not found"** → verify the top-level key in your JSON matches the internal name passed to `@register_theme`, and the JSON is valid (no trailing commas)
- **Theme not in dropdown** → check that `DISPLAY_NAME` is set on the handler class
- **Theme not in Multiple Prompt Generator** → add its display name to a category in `theme_categories` (`mega_prompt_all_themes.py`)