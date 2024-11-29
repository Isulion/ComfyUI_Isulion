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

# New Holiday Theme Handlers
from .easter_handler import EasterThemeHandler
from .valentines_day_handler import ValentinesDayThemeHandler
from .new_years_eve_handler import NewYearsEveThemeHandler
from .thanksgiving_handler import ThanksgivingThemeHandler
from .st_patricks_day_handler import StPatricksDayThemeHandler
from .dia_de_los_muertos_handler import DiaDeLosmuertosThemeHandler
from .chinese_new_year_handler import ChineseNewYearThemeHandler

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
    'WatercolorThemeHandler',
    # New Holiday Theme Handlers
    'EasterThemeHandler',
    'ValentinesDayThemeHandler',
    'NewYearsEveThemeHandler',
    'ThanksgivingThemeHandler',
    'StPatricksDayThemeHandler',
    'DiaDeLosmuertosThemeHandler',
    'ChineseNewYearThemeHandler'
]
