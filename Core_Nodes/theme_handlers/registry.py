"""Decorator-based registry for Isulion theme handlers.

Usage:
    @register_theme("abstract")
    class AbstractThemeHandler(BaseThemeHandler):
        ...

The registry removes the need for star-imports, string-based class lookups
via globals(), and a hand-maintained name mapping table.
"""

from typing import Dict, Type

THEME_HANDLERS: Dict[str, Type] = {}


def register_theme(internal_name: str):
    """Class decorator registering a theme handler under its internal name."""
    def decorator(cls):
        if internal_name in THEME_HANDLERS:
            raise ValueError(
                f"Duplicate theme registration '{internal_name}' "
                f"({THEME_HANDLERS[internal_name].__name__} vs {cls.__name__})"
            )
        THEME_HANDLERS[internal_name] = cls
        return cls
    return decorator
