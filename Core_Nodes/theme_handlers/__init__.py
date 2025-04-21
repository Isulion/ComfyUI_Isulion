"""Theme handlers package initialization."""

# Base handler
from .base_handler import BaseThemeHandler

# Art Style Handlers
from .abstract_handler import AbstractThemeHandler
from .animation_cartoon_handler import AnimationCartoonThemeHandler
from .anime_handler import AnimeThemeHandler
from .architectural_handler import ArchitecturalThemeHandler
from .bio_organic_tech_handler import BioOrganicTechThemeHandler
from .binet_surreal_handler import BinetSurrealThemeHandler
from .caricature_handler import CaricatureThemeHandler
from .character_designer_handler import CharacterDesignerThemeHandler
from .clay_art_handler import ClayArtThemeHandler
from .comic_book_handler import ComicBookThemeHandler
from .concept_art_handler import ConceptArtThemeHandler
from .crayon_art_handler import CrayonArtThemeHandler
from .digital_art_handler import DigitalArtThemeHandler
from .dimension_3d_handler import Dimension3DThemeHandler
from .experimental_art_handler import ExperimentalArtThemeHandler
from .impressionist_handler import ImpressionistThemeHandler
from .minimalist_handler import MinimalistThemeHandler
from .nature_handler import NatureThemeHandler
from .spectral_mist_handler import SpectralMistThemeHandler
from .stopmotion_handler import StopMotionThemeHandler
from .watercolor_handler import WatercolorThemeHandler

# Genre Handlers
from .cyberpunk_handler import CyberpunkThemeHandler
from .crystalpunk_handler import CrystalpunkThemeHandler
from .fantasy_handler import FantasyThemeHandler
from .horror_handler import HorrorThemeHandler
from .scifi_handler import SciFiThemeHandler
from .steampunk_handler import SteampunkThemeHandler

# Studio and Brand Handlers
from .disney_handler import DisneyThemeHandler
from .dreamworks_handler import DreamworksThemeHandler
from .ghibli_handler import GhibliThemeHandler
from .marvel_handler import MarvelThemeHandler
from .nolan_handler import NolanThemeHandler
from .miura_handler import MiuraThemeHandler
from .pixar_handler import PixarThemeHandler
from .star_wars_handler import StarWarsThemeHandler

# Theme and Setting Handlers
from .chimera_animals_handler import ChimeraAnimalsThemeHandler
from .chimera_cute_animals_handler import ChimeraCuteAnimalsThemeHandler
from .culinary_food_handler import CulinaryFoodThemeHandler
from .curvy_fashion_handler import CurvyFashionThemeHandler
from .enchanted_fantasy_handler import EnchantedFantasyThemeHandler
from .essential_realistic_handler import EssentialRealisticThemeHandler
from .essential_vintage_handler import EssentialVintageThemeHandler
from .ethereal_dreams_handler import EtherealDreamsThemeHandler
from .fifties_commercial_handler import FiftiesCommercialHandler
from .futuristic_battlefield_handler import FuturisticBattlefieldThemeHandler
from .futuristic_city_handler import FuturisticCityThemeHandler
from .futuristic_city_metropolis_handler import FuturisticCityMetropolisThemeHandler
from .futuristic_scifi_handler import FuturisticSciFiThemeHandler
from .interior_spaces_handler import InteriorSpacesThemeHandler
from .logo_handler import LogoThemeHandler
from .manga_panel_handler import MangaPanelThemeHandler
from .microscopic_handler import MicroscopicThemeHandler
from .peaky_blinders_handler import PeakyBlindersThemeHandler
from .post_apocalyptic_handler import PostApocalypticThemeHandler
from .puzzle_dimension_handler import PuzzleDimensionThemeHandler
from .school_manga_handler import SchoolMangaThemeHandler
from .selfie_handler import SelfieThemeHandler
from .skinny_blonde_girl_handler import SkinnyBlondeGirlHandler
from .street_food_kebab_handler import StreetFoodKebabThemeHandler
from .underwater_civilization_handler import UnderwaterCivilizationThemeHandler
from .urban_tag_handler import UrbanTagThemeHandler
from .village_world_handler import VillageWorldThemeHandler
from .vintage_anthropomorphic_handler import VintageAnthropomorphicThemeHandler
from .vintage_1800s_photography_handler import Vintage1800sPhotographyHandler
from .historical_monuments_handler import HistoricalMonumentsHandler
from .medieval_handler import MedievalThemeHandler

# Holiday and Event Handlers
from .chinese_new_year_handler import ChineseNewYearThemeHandler
from .christmas_handler import ChristmasThemeHandler
from .dia_de_los_muertos_handler import DiaDeLosmuertosThemeHandler
from .easter_handler import EasterThemeHandler
from .halloween_handler import HalloweenThemeHandler
from .halloween_ethereal_handler import HalloweenEtherealThemeHandler
from .new_years_eve_handler import NewYearsEveThemeHandler
from .st_patricks_day_handler import StPatricksDayThemeHandler
from .thanksgiving_handler import ThanksgivingThemeHandler
from .valentines_day_handler import ValentinesDayThemeHandler

# Cinema and Media Handlers
from .cinema_studio_handler import CinemaStudioThemeHandler
from .instagram_handler import InstagramThemeHandler
from .instagram_lifestyle_handler import InstagramLifestyleThemeHandler

# Export all handlers
__all__ = [
    # Base Handler
    'BaseThemeHandler',
    
    # Art Style Handlers
    'AbstractThemeHandler', 'AnimationCartoonThemeHandler', 'AnimeThemeHandler',
    'ArchitecturalThemeHandler', 'BioOrganicTechThemeHandler', 'BinetSurrealThemeHandler',
    'CaricatureThemeHandler', 'CharacterDesignerThemeHandler', 'ClayArtThemeHandler',
    'ComicBookThemeHandler', 'ConceptArtThemeHandler', 'CrayonArtThemeHandler',
    'DigitalArtThemeHandler', 'Dimension3DThemeHandler', 'ExperimentalArtThemeHandler',
    'ImpressionistThemeHandler', 'MinimalistThemeHandler', 'NatureThemeHandler', 'SpectralMistThemeHandler',
    'StopMotionThemeHandler', 'WatercolorThemeHandler',
    
    # Genre Handlers
    'CyberpunkThemeHandler', 'CrystalpunkThemeHandler', 'FantasyThemeHandler',
    'HorrorThemeHandler', 'SciFiThemeHandler', 'SteampunkThemeHandler',
    
    # Studio and Brand Handlers
    'DisneyThemeHandler', 'DreamworksThemeHandler', 'GhibliThemeHandler',
    'MarvelThemeHandler', 'NolanThemeHandler', 'MiuraThemeHandler',
    'PixarThemeHandler', 'StarWarsThemeHandler',
    
    # Theme and Setting Handlers
    'ChimeraAnimalsThemeHandler', 'ChimeraCuteAnimalsThemeHandler',
    'CulinaryFoodThemeHandler', 'CurvyFashionThemeHandler',
    'EnchantedFantasyThemeHandler', 'EssentialRealisticThemeHandler',
    'EssentialVintageThemeHandler', 'EtherealDreamsThemeHandler',
    'FiftiesCommercialHandler', 'FuturisticBattlefieldThemeHandler',
    'FuturisticCityThemeHandler', 'FuturisticCityMetropolisThemeHandler',
    'FuturisticSciFiThemeHandler', 'InteriorSpacesThemeHandler',
    'LogoThemeHandler', 'MangaPanelThemeHandler', 'MicroscopicThemeHandler',
    'PeakyBlindersThemeHandler', 'PostApocalypticThemeHandler',
    'PuzzleDimensionThemeHandler', 'SchoolMangaThemeHandler',
    'SelfieThemeHandler', 'SkinnyBlondeGirlHandler', 'StreetFoodKebabThemeHandler',
    'UnderwaterCivilizationThemeHandler', 'UrbanTagThemeHandler',
    'VillageWorldThemeHandler', 'VintageAnthropomorphicThemeHandler',
    'Vintage1800sPhotographyHandler', 'HistoricalMonumentsHandler',
    'MedievalThemeHandler',
    
    # Holiday and Event Handlers
    'ChineseNewYearThemeHandler', 'ChristmasThemeHandler',
    'DiaDeLosmuertosThemeHandler', 'EasterThemeHandler',
    'HalloweenThemeHandler', 'HalloweenEtherealThemeHandler',
    'NewYearsEveThemeHandler', 'StPatricksDayThemeHandler',
    'ThanksgivingThemeHandler', 'ValentinesDayThemeHandler',
    
    # Cinema and Media Handlers
    'CinemaStudioThemeHandler', 'InstagramThemeHandler',
    'InstagramLifestyleThemeHandler',
    
    # Historical and Period Handlers
    'HistoricalMonumentsHandler',
    'MedievalThemeHandler'
]
