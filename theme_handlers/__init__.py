"""Theme handlers package initialization."""

from .base_handler import BaseThemeHandler
from .abstract_handler import AbstractThemeHandler
from .anime_handler import AnimeThemeHandler
from .scifi_handler import SciFiThemeHandler
from .pixar_handler import PixarThemeHandler
from .fantasy_handler import FantasyThemeHandler
from .cyberpunk_handler import CyberpunkThemeHandler
from .ghibli_handler import GhibliThemeHandler
from .horror_handler import HorrorThemeHandler
from .steampunk_handler import SteampunkThemeHandler
from .watercolor_handler import WatercolorThemeHandler

__all__ = [
    'BaseThemeHandler',
    'AbstractThemeHandler',
    'AnimeThemeHandler',
    'SciFiThemeHandler',
    'PixarThemeHandler',
    'FantasyThemeHandler',
    'CyberpunkThemeHandler',
    'GhibliThemeHandler',
    'HorrorThemeHandler',
    'SteampunkThemeHandler',
    'WatercolorThemeHandler'
]
