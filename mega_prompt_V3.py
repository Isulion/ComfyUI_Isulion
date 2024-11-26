import random
import os
from typing import Dict, List, Tuple, Optional
from .configs.config_manager import ConfigManager
from .theme_handlers.base_handler import BaseThemeHandler
from .theme_handlers.anime_handler import AnimeThemeHandler
from .theme_handlers.abstract_handler import AbstractThemeHandler
from .theme_handlers.scifi_handler import SciFiThemeHandler
from .theme_handlers.pixar_handler import PixarThemeHandler
from .theme_handlers.fantasy_handler import FantasyThemeHandler
from .theme_handlers.cyberpunk_handler import CyberpunkThemeHandler
from .theme_handlers.ghibli_handler import GhibliThemeHandler
from .theme_handlers.horror_handler import HorrorThemeHandler
from .theme_handlers.steampunk_handler import SteampunkThemeHandler
from .theme_handlers.watercolor_handler import WatercolorThemeHandler
from .theme_handlers.logo_handler import LogoThemeHandler
from .theme_handlers.caricature_handler import CaricatureThemeHandler
from .theme_handlers.futuristic_city_handler import FuturisticCityThemeHandler
from .theme_handlers.halloween_handler import HalloweenThemeHandler
from .theme_handlers.instagram_handler import InstagramThemeHandler
from .theme_handlers.marvel_handler import MarvelThemeHandler
from .theme_handlers.microscopic_handler import MicroscopicThemeHandler
from .theme_handlers.minimalist_handler import MinimalistThemeHandler
from .theme_handlers.animation_cartoon_handler import AnimationCartoonThemeHandler
from .theme_handlers.architectural_handler import ArchitecturalThemeHandler
from .theme_handlers.bio_organic_tech_handler import BioOrganicTechThemeHandler
from .theme_handlers.binet_surreal_handler import BinetSurrealThemeHandler
from .theme_handlers.chimera_animals_handler import ChimeraAnimalsThemeHandler
from .theme_handlers.chimera_cute_animals_handler import ChimeraCuteAnimalsThemeHandler
from .theme_handlers.christmas_handler import ChristmasThemeHandler
from .theme_handlers.cinema_studio_handler import CinemaStudioThemeHandler
from .theme_handlers.clay_art_handler import ClayArtThemeHandler
from .theme_handlers.comic_book_handler import ComicBookThemeHandler
from .theme_handlers.concept_art_handler import ConceptArtThemeHandler
from .theme_handlers.crayon_art_handler import CrayonArtThemeHandler
from .theme_handlers.crystalpunk_handler import CrystalpunkThemeHandler
from .theme_handlers.culinary_food_handler import CulinaryFoodThemeHandler
from .theme_handlers.curvy_fashion_handler import CurvyFashionThemeHandler
from .theme_handlers.digital_art_handler import DigitalArtThemeHandler
from .theme_handlers.dimension_3d_handler import Dimension3DThemeHandler
from .theme_handlers.enchanted_fantasy_handler import EnchantedFantasyThemeHandler
from .theme_handlers.essential_realistic_handler import EssentialRealisticThemeHandler
from .theme_handlers.essential_vintage_handler import EssentialVintageThemeHandler
from .theme_handlers.ethereal_dreams_handler import EtherealDreamsThemeHandler
from .theme_handlers.experimental_art_handler import ExperimentalArtThemeHandler
from .theme_handlers.futuristic_battlefield_handler import FuturisticBattlefieldThemeHandler
from .theme_handlers.futuristic_city_metropolis_handler import FuturisticCityMetropolisThemeHandler
from .theme_handlers.futuristic_scifi_handler import FuturisticSciFiThemeHandler
from .theme_handlers.halloween_ethereal_handler import HalloweenEtherealThemeHandler
from .theme_handlers.impressionist_handler import ImpressionistThemeHandler
from .theme_handlers.instagram_lifestyle_handler import InstagramLifestyleThemeHandler
from .theme_handlers.manga_panel_handler import MangaPanelThemeHandler
from .theme_handlers.peaky_blinders_handler import PeakyBlindersThemeHandler
from .theme_handlers.post_apocalyptic_handler import PostApocalypticThemeHandler
from .theme_handlers.school_manga_handler import SchoolMangaThemeHandler
from .theme_handlers.star_wars_handler import StarWarsThemeHandler
from .theme_handlers.underwater_civilization_handler import UnderwaterCivilizationThemeHandler
from .theme_handlers.urban_tag_handler import UrbanTagThemeHandler
from .theme_handlers.village_world_handler import VillageWorldThemeHandler
from .theme_handlers.vintage_anthropomorphic_handler import VintageAnthropomorphicThemeHandler
from .theme_handlers.selfie_handler import SelfieThemeHandler

class MegaPromptV3:
    """
    Enhanced version of the Mega Prompt Generator with improved organization and features.
    """
    
    def __init__(self):
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize theme handlers
        self._init_theme_handlers()
        
        # Initialize theme mappings
        self.theme_mappings = {
            "🎲 Dynamic Random": "random",
            "🎨 Abstract": "abstract",
            "📺 Animation Cartoon": "animation_cartoon",
            "🎌 Anime": "anime",
            "🏛️ Architectural": "architectural",
            "🧬 Bio-Organic Technology": "bio_organic_tech",
            "🖼️ Binet Surreal": "binet_surreal",
            "😄 Caricature": "caricature",
            "🦄 Chimera Animals": "chimera_animals",
            "🐰 Chimera Cute Animals": "chimera_cute_animals",
            "🎄 Christmas": "christmas",
            "🎬 Cinema Studio": "cinema_studio",
            "🏺 Clay Art": "clay_art",
            "📚 Comic Book": "comic_book",
            "🎨 Concept Art": "concept_art",
            "🖍️ Crayon Art": "crayon_art",
            "💎 Crystalpunk": "crystalpunk",
            "🌆 Cyberpunk": "cyberpunk",
            "🍳 Culinary/Food": "culinary_food",
            "👗 Curvy Fashion": "curvy_fashion",
            "💻 Digital Art": "digital_art",
            "💠 Dimension 3D": "dimension_3d",
            "✨ Enchanted Fantasy": "enchanted_fantasy",
            "📸 Essential Realistic": "essential_realistic",
            "🕰️ Essential Vintage": "essential_vintage",
            "💫 Ethereal Dreams": "ethereal_dreams",
            "🔬 Experimental Art": "experimental_art",
            "⚔️ Fantasy": "fantasy",
            "🌃 Futuristic City": "futuristic_city",
            "⚔️ Futuristic Battlefield": "futuristic_battlefield",
            "🌆 Futuristic City Metropolis": "futuristic_city_metropolis",
            "🚀 Futuristic Sci-Fi": "futuristic_scifi",
            "🍃 Ghibli": "ghibli",
            "🎃 Halloween": "halloween",
            "👻 Halloween Ethereal": "halloween_ethereal",
            "👻 Horror": "horror",
            "🎨 Impressionist": "impressionist",
            "📱 Instagram": "instagram",
            "📱 Instagram Lifestyle": "instagram_lifestyle",
            "🎯 Logo": "logo",
            "📺 Manga Panel": "manga_panel",
            "🦸 Marvel": "marvel",
            "🔬 Microscopic": "microscopic",
            "⬜ Minimalist": "minimalist",
            "🕴️‍♂️ Peaky Blinders": "peaky_blinders",
            "💫 Pixar": "pixar",
            "🌪️ Post Apocalyptic": "post_apocalyptic",
            "🚀 Sci-Fi": "scifi",
            "📚 School Manga": "school_manga",
            "📱 Selfie": "selfie",
            "🚀 Star Wars": "star_wars",
            "⚙️ Steampunk": "steampunk",
            "🌊 Underwater Civilization": "underwater_civilization",
            "🏙️ Urban Tag": "urban_tag",
            "🏠 Village World": "village_world",
            "👴 Vintage Anthropomorphic": "vintage_anthropomorphic",
            "🎨 Watercolor": "watercolor"
        }
    
    def _init_theme_handlers(self):
        """Initialize all theme handlers."""
        self.handlers = {
            "abstract": AbstractThemeHandler(self.config_manager),
            "animation_cartoon": AnimationCartoonThemeHandler(self.config_manager),
            "anime": AnimeThemeHandler(self.config_manager),
            "architectural": ArchitecturalThemeHandler(self.config_manager),
            "bio_organic_tech": BioOrganicTechThemeHandler(self.config_manager),
            "binet_surreal": BinetSurrealThemeHandler(self.config_manager),
            "caricature": CaricatureThemeHandler(self.config_manager),
            "chimera_animals": ChimeraAnimalsThemeHandler(self.config_manager),
            "chimera_cute_animals": ChimeraCuteAnimalsThemeHandler(self.config_manager),
            "christmas": ChristmasThemeHandler(self.config_manager),
            "cinema_studio": CinemaStudioThemeHandler(self.config_manager),
            "clay_art": ClayArtThemeHandler(self.config_manager),
            "comic_book": ComicBookThemeHandler(self.config_manager),
            "concept_art": ConceptArtThemeHandler(self.config_manager),
            "crayon_art": CrayonArtThemeHandler(self.config_manager),
            "crystalpunk": CrystalpunkThemeHandler(self.config_manager),
            "cyberpunk": CyberpunkThemeHandler(self.config_manager),
            "culinary_food": CulinaryFoodThemeHandler(self.config_manager),
            "curvy_fashion": CurvyFashionThemeHandler(self.config_manager),
            "digital_art": DigitalArtThemeHandler(self.config_manager),
            "dimension_3d": Dimension3DThemeHandler(self.config_manager),
            "enchanted_fantasy": EnchantedFantasyThemeHandler(self.config_manager),
            "essential_realistic": EssentialRealisticThemeHandler(self.config_manager),
            "essential_vintage": EssentialVintageThemeHandler(self.config_manager),
            "ethereal_dreams": EtherealDreamsThemeHandler(self.config_manager),
            "experimental_art": ExperimentalArtThemeHandler(self.config_manager),
            "fantasy": FantasyThemeHandler(self.config_manager),
            "futuristic_battlefield": FuturisticBattlefieldThemeHandler(self.config_manager),
            "futuristic_city": FuturisticCityThemeHandler(self.config_manager),
            "futuristic_city_metropolis": FuturisticCityMetropolisThemeHandler(self.config_manager),
            "futuristic_scifi": FuturisticSciFiThemeHandler(self.config_manager),
            "ghibli": GhibliThemeHandler(self.config_manager),
            "halloween": HalloweenThemeHandler(self.config_manager),
            "halloween_ethereal": HalloweenEtherealThemeHandler(self.config_manager),
            "horror": HorrorThemeHandler(self.config_manager),
            "impressionist": ImpressionistThemeHandler(self.config_manager),
            "instagram": InstagramThemeHandler(self.config_manager),
            "instagram_lifestyle": InstagramLifestyleThemeHandler(self.config_manager),
            "logo": LogoThemeHandler(self.config_manager),
            "manga_panel": MangaPanelThemeHandler(self.config_manager),
            "marvel": MarvelThemeHandler(self.config_manager),
            "microscopic": MicroscopicThemeHandler(self.config_manager),
            "minimalist": MinimalistThemeHandler(self.config_manager),
            "peaky_blinders": PeakyBlindersThemeHandler(self.config_manager),
            "pixar": PixarThemeHandler(self.config_manager),
            "post_apocalyptic": PostApocalypticThemeHandler(self.config_manager),
            "scifi": SciFiThemeHandler(self.config_manager),
            "school_manga": SchoolMangaThemeHandler(self.config_manager),
            "selfie": SelfieThemeHandler(self.config_manager),
            "star_wars": StarWarsThemeHandler(self.config_manager),
            "steampunk": SteampunkThemeHandler(self.config_manager),
            "underwater_civilization": UnderwaterCivilizationThemeHandler(self.config_manager),
            "urban_tag": UrbanTagThemeHandler(self.config_manager),
            "village_world": VillageWorldThemeHandler(self.config_manager),
            "vintage_anthropomorphic": VintageAnthropomorphicThemeHandler(self.config_manager),
            "watercolor": WatercolorThemeHandler(self.config_manager)
        }
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """Define input types for the node."""
        return {
            "required": {
                "theme": ([
                    "🎲 Dynamic Random",  # Keeps Random at top
                    "🎨 Abstract",
                    "📺 Animation Cartoon",
                    "🎌 Anime",
                    "🏛️ Architectural",
                    "🧬 Bio-Organic Technology",
                    "🖼️ Binet Surreal",
                    "😄 Caricature",
                    "🦄 Chimera Animals",
                    "🐰 Chimera Cute Animals",
                    "🎄 Christmas",
                    "🎬 Cinema Studio",
                    "🏺 Clay Art",
                    "📚 Comic Book",
                    "🎨 Concept Art",
                    "🖍️ Crayon Art",
                    "💎 Crystalpunk",
                    "🍳 Culinary/Food",
                    "🌆 Cyberpunk",
                    "👗 Curvy Fashion",
                    "💻 Digital Art",
                    "💠 Dimension 3D",
                    "✨ Enchanted Fantasy",
                    "📸 Essential Realistic",
                    "🕰️ Essential Vintage",
                    "💫 Ethereal Dreams",
                    "🔬 Experimental Art",
                    "⚔️ Fantasy",
                    "🌃 Futuristic City",
                    "⚔️ Futuristic Battlefield",
                    "🌆 Futuristic City Metropolis",
                    "🚀 Futuristic Sci-Fi",
                    "🍃 Ghibli",
                    "🎃 Halloween",
                    "👻 Halloween Ethereal",
                    "👻 Horror",
                    "🎨 Impressionist",
                    "📱 Instagram",
                    "📱 Instagram Lifestyle",
                    "🎯 Logo",
                    "📺 Manga Panel",
                    "🦸 Marvel",
                    "🔬 Microscopic",
                    "⬜ Minimalist",
                    "🕴️‍♂️ Peaky Blinders",
                    "💫 Pixar",
                    "🌪️ Post Apocalyptic",
                    "🚀 Sci-Fi",
                    "📚 School Manga",
                    "🚀 Star Wars",
                    "⚙️ Steampunk",
                    "🌊 Underwater Civilization",
                    "🏙️ Urban Tag",
                    "🏠 Village World",
                    "👴 Vintage Anthropomorphic",
                    "🎨 Watercolor",
                    "📱 Selfie"
                ], {"default": "🎲 Dynamic Random"}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "custom_location": ("STRING", {"default": "", "multiline": True}),
                "include_environment": (["yes", "no"], {"default": "yes"}),
                "include_style": (["yes", "no"], {"default": "yes"}),
                "include_effects": (["yes", "no"], {"default": "yes"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "subject", "environment", "style", "effects", "seed")
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, theme: str, complexity: str = "detailed", randomize: str = "enable",
                seed: int = 0, custom_subject: str = "", custom_location: str = "",
                include_environment: str = "yes", include_style: str = "yes",
                include_effects: str = "yes") -> Tuple[str, str, str, str, str, int]:
        """Generate a prompt based on the given parameters."""
        try:
            # Set seed if randomization is disabled
            if randomize == "disable":
                self.config_manager.set_seed(seed)
            
            # Map theme to internal name
            internal_theme = self.theme_mappings.get(theme, "random")
            
            # Get appropriate handler
            if internal_theme == "random":
                # Exclude "random" from possible choices
                available_themes = [k for k in self.handlers.keys() if k != "random"]
                if not available_themes:
                    print("Warning: No theme handlers available, using default handler")
                    internal_theme = "abstract"  # Use abstract as fallback
                else:
                    internal_theme = self.config_manager.random.choice(available_themes)
            
            handler = self.handlers.get(internal_theme)
            if not handler:
                print(f"Warning: No handler found for theme {internal_theme}, using abstract handler")
                handler = self.handlers.get("abstract", AbstractThemeHandler(self.config_manager))
            
            # Generate components
            try:
                components = handler.generate(
                    custom_subject=custom_subject,
                    custom_location=custom_location,
                    include_environment=include_environment,
                    include_style=include_style,
                    include_effects=include_effects
                )
            except Exception as e:
                print(f"Error generating components with {internal_theme} handler: {str(e)}")
                # Only fallback to abstract for themes that should be abstract
                if internal_theme not in ["peaky_blinders", "essential_realistic", "essential_vintage", "cinema_studio"]:
                    print("Falling back to abstract handler")
                    handler = AbstractThemeHandler(self.config_manager)
                    components = handler.generate(
                        custom_subject=custom_subject,
                        custom_location=custom_location,
                        include_environment=include_environment,
                        include_style=include_style,
                        include_effects=include_effects
                    )
                else:
                    # For realistic themes, provide a safe fallback that maintains theme
                    print(f"Using safe fallback for {internal_theme}")
                    components = {
                        "subject": f"((a detailed {internal_theme.replace('_', ' ')} style portrait))",
                        "environment": "in a thematically appropriate setting",
                        "style": "with professional quality and theme-specific details",
                        "effects": "with refined details and appropriate effects"
                    }
            
            # Ensure all components exist
            default_components = {
                "subject": "a detailed subject",
                "environment": "in a detailed environment",
                "style": "with professional quality",
                "effects": "with refined details",
            }
            for key in default_components:
                if key not in components:
                    components[key] = default_components[key]
            
            # Build final prompt
            prompt = ", ".join(filter(None, [
                components.get("subject", ""),
                components.get("environment", "") if include_environment == "yes" else "",
                components.get("style", "") if include_style == "yes" else "",
                components.get("effects", "") if include_effects == "yes" else ""
            ]))
            
            return (
                prompt,
                components.get("subject", ""),
                components.get("environment", ""),
                components.get("style", ""),
                components.get("effects", ""),
                seed
            )
            
        except Exception as e:
            print(f"Error in generate method: {str(e)}")
            # Return safe default values
            return (
                "a detailed subject in a professional environment",
                "a detailed subject",
                "in a professional environment",
                "with professional quality",
                "with refined details",
                seed
            )
