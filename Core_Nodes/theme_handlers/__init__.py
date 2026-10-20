"""Theme handlers package: auto-discovers all handler modules.

Every handler module imports @register_theme and registers itself at import
time, so adding a new theme never requires touching this file.
"""

import importlib
import pkgutil

from .base_handler import BaseThemeHandler


def _load_all_handler_modules() -> None:
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name in ("base_handler", "registry"):
            continue
        importlib.import_module(f"{__name__}.{module_info.name}")


_load_all_handler_modules()

__all__ = ["BaseThemeHandler"]
