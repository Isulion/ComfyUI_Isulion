import random
import os
from typing import Dict, List, Tuple, Optional

# Config imports
from .configs.config_manager import ConfigManager

# Import all theme handlers
from .theme_handlers import *

class ThemeRegistry:
    """Registry for managing theme handlers and their mappings."""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.handlers = {}
        self.theme_mappings = {}
        self._init_handlers()
        self._init_mappings()

    def _init_handlers(self):
        """Initialize all theme handlers with a more maintainable approach."""
        handler_classes = {
            "abstract": AbstractThemeHandler,
            "animation_cartoon": AnimationCartoonThemeHandler,
            "anime": AnimeThemeHandler,
            "architectural": ArchitecturalThemeHandler,
            "bio_organic_tech": BioOrganicTechThemeHandler,
            "binet_surreal": BinetSurrealThemeHandler,
            "caricature": CaricatureThemeHandler,
            "chimera_animals": ChimeraAnimalsThemeHandler,
            "chimera_cute_animals": ChimeraCuteAnimalsThemeHandler,
            "christmas": ChristmasThemeHandler,
            "cinema_studio": CinemaStudioThemeHandler,
            "clay_art": ClayArtThemeHandler,
            "comic_book": ComicBookThemeHandler,
            "character_designer": CharacterDesignerThemeHandler,
            "chinese_new_year": ChineseNewYearThemeHandler,
            "concept_art": ConceptArtThemeHandler,
            "crayon_art": CrayonArtThemeHandler,
            "crystalpunk": CrystalpunkThemeHandler,
            "cyberpunk": CyberpunkThemeHandler,
            "culinary_food": CulinaryFoodThemeHandler,
            "curvy_fashion": CurvyFashionThemeHandler,
            "dia_de_los_muertos": DiaDeLosmuertosThemeHandler,
            "digital_art": DigitalArtThemeHandler,
            "disney": DisneyThemeHandler,
            "dreamworks": DreamworksThemeHandler,
            "dimension_3d": Dimension3DThemeHandler,
            "easter": EasterThemeHandler,
            "enchanted_fantasy": EnchantedFantasyThemeHandler,
            "essential_realistic": EssentialRealisticThemeHandler,
            "essential_vintage": EssentialVintageThemeHandler,
            "ethereal_dreams": EtherealDreamsThemeHandler,
            "experimental_art": ExperimentalArtThemeHandler,
            "fantasy": FantasyThemeHandler,
            "fifties_commercial": FiftiesCommercialHandler,
            "futuristic_battlefield": FuturisticBattlefieldThemeHandler,
            "futuristic_city": FuturisticCityThemeHandler,
            "futuristic_city_metropolis": FuturisticCityMetropolisThemeHandler,
            "futuristic_scifi": FuturisticSciFiThemeHandler,
            "ghibli": GhibliThemeHandler,
            "halloween": HalloweenThemeHandler,
            "halloween_ethereal": HalloweenEtherealThemeHandler,
            "historical_monuments": HistoricalMonumentsHandler,
            "horror": HorrorThemeHandler,
            "impressionist": ImpressionistThemeHandler,
            "instagram": InstagramThemeHandler,
            "instagram_lifestyle": InstagramLifestyleThemeHandler,
            "interior_spaces": InteriorSpacesThemeHandler,
            "logo": LogoThemeHandler,
            "manga_panel": MangaPanelThemeHandler,
            "marvel": MarvelThemeHandler,
            "medieval": MedievalThemeHandler,
            "microscopic": MicroscopicThemeHandler,
            "minimalist": MinimalistThemeHandler,
            "miura": MiuraThemeHandler,
            "nature": NatureThemeHandler,
            "new_years_eve": NewYearsEveThemeHandler,
            "nolan": NolanThemeHandler,
            "peaky_blinders": PeakyBlindersThemeHandler,
            "pixar": PixarThemeHandler,
            "post_apocalyptic": PostApocalypticThemeHandler,
            "puzzle_dimension": PuzzleDimensionThemeHandler,
            "scifi": SciFiThemeHandler,
            "school_manga": SchoolMangaThemeHandler,
            "selfie": SelfieThemeHandler,
            "Spartan 300": s300ThemeHandler,
            "spectral_mist": SpectralMistThemeHandler,
            "st_patricks_day": StPatricksDayThemeHandler,            
            "star_wars": StarWarsThemeHandler,
            "steampunk": SteampunkThemeHandler,
            "stopmotion": StopMotionThemeHandler,
            "street_food_kebab": StreetFoodKebabThemeHandler,
            "thanksgiving": ThanksgivingThemeHandler,
            "underwater_civilization": UnderwaterCivilizationThemeHandler,
            "urban_tag": UrbanTagThemeHandler,
            "valentines_day": ValentinesDayThemeHandler,
            "village_world": VillageWorldThemeHandler,
            "vintage_1800s_photography": Vintage1800sPhotographyHandler,
            "vintage_anthropomorphic": VintageAnthropomorphicThemeHandler,
            "watercolor": WatercolorThemeHandler,
            "street_food_kebab": StreetFoodKebabThemeHandler,
            "easter": EasterThemeHandler,
            "valentines_day": ValentinesDayThemeHandler,
            "new_years_eve": NewYearsEveThemeHandler,
            "thanksgiving": ThanksgivingThemeHandler,
            "st_patricks_day": StPatricksDayThemeHandler,
            "dia_de_los_muertos": DiaDeLosmuertosThemeHandler,
            "chinese_new_year": ChineseNewYearThemeHandler,
            "spectral_mist": SpectralMistThemeHandler,
            "vintage_1800s_photography": Vintage1800sPhotographyHandler,
            "historical_monuments": HistoricalMonumentsHandler,
            "medieval": MedievalThemeHandler,
            "skinny_blonde_girl": SkinnyBlondeGirlHandler,
        }
        
        self.handlers = {
            name: handler_class(self.config_manager)
            for name, handler_class in handler_classes.items()
        }
    
    def _init_mappings(self):
        """Initialize theme mappings with emojis."""
        emoji_mappings = {
            "🎲 Dynamic Random": "random",
            "🧺 50s Commercial": "fifties_commercial",
            "🎨 Abstract": "abstract",
            "📺 Animation Cartoon": "animation_cartoon",
            "🎌 Anime": "anime",
            "🏛️ Architectural": "architectural",
            "🧬 Bio-Organic Technology": "bio_organic_tech",
            "🖼️ Binet Surreal": "binet_surreal",
            "😄 Caricature": "caricature",
            "👤 Character Designer": "character_designer",
            "🦄 Chimera Animals": "chimera_animals",
            "🐰 Chimera Cute Animals": "chimera_cute_animals",
            "🏮 Chinese New Year": "chinese_new_year",
            "🎄 Christmas": "christmas",
            "🎬 Cinema Studio": "cinema_studio",
            "🏺 Clay Art": "clay_art",
            "📚 Comic Book": "comic_book",
            "🎨 Concept Art": "concept_art",
            "🖍️ Crayon Art": "crayon_art",
            "💎 Crystalpunk": "crystalpunk",
            "🍳 Culinary/Food": "culinary_food",
            "👗 Curvy Fashion": "curvy_fashion",
            "🌆 Cyberpunk": "cyberpunk",
            "👹 Dia de los Muertos": "dia_de_los_muertos",
            "💠 Dimension 3D": "dimension_3d",
            "🖼️ Digital Art": "digital_art",
            "🎡 Disney": "disney",
            "🎬 Dreamworks": "dreamworks",
            "🐰 Easter": "easter",
            "✨ Enchanted Fantasy": "enchanted_fantasy",
            "📸 Essential Realistic": "essential_realistic",
            "🕰️ Essential Vintage": "essential_vintage",
            "✨ Ethereal Dreams": "ethereal_dreams",
            "🔬 Experimental Art": "experimental_art",
            "⚔️ Fantasy": "fantasy",
            "🌆 Futuristic City": "futuristic_city",
            "⚔️ Futuristic Battlefield": "futuristic_battlefield",
            "🌆 Futuristic City Metropolis": "futuristic_city_metropolis",
            "🚀 Futuristic Sci-Fi": "futuristic_scifi",
            "🍃 Ghibli": "ghibli",
            "🎃 Halloween": "halloween",
            "👻 Halloween Ethereal": "halloween_ethereal",
            "🏛️ Historical Monuments": "historical_monuments",
            "👻 Horror": "horror",
            "🎨 Impressionist": "impressionist",
            "📱 Instagram": "instagram",
            "📱 Instagram Lifestyle": "instagram_lifestyle",
            "🏠 Interior Spaces": "interior_spaces",
            "🎯 Logo": "logo",
            "📺 Manga Panel": "manga_panel",
            "🦸 Marvel": "marvel",
            "⚔️ Medieval": "medieval",
            "🔬 Microscopic": "microscopic",
            "⬜ Minimalist": "minimalist",
            "⚔️ Miura Dark Fantasy": "miura",
            "🌿 Nature": "nature",
            "🎆 New Year's Eve": "new_years_eve",
            "🎬 Nolan Epic": "nolan",
            "🕴️ Peaky Blinders": "peaky_blinders",
            "💫 Pixar": "pixar",
            "🌪️ Post Apocalyptic": "post_apocalyptic",
            "🧩 Puzzle Dimension": "puzzle_dimension",
            "🚀 Sci-Fi": "scifi",
            "📚 School Manga": "school_manga",
            "📱 Selfie": "selfie",
            "👧💃 Skinny Blonde Girl": "skinny_blonde_girl",
            "💗 Spectral Mist": "spectral_mist",
            "🍀 St. Patrick's Day": "st_patricks_day",
            "🚀 Star Wars": "star_wars",
            "⚙️ Steampunk": "steampunk",
            "🎭 Stop Motion": "stopmotion",
            "🥙 Street Food Kebab": "street_food_kebab",
            "🦃 Thanksgiving": "thanksgiving",
            "🌊 Underwater Civilization": "underwater_civilization",
            "🏙️ Urban Tag": "urban_tag",
            "💘 Valentine's Day": "valentines_day",
            "🏠 Village World": "village_world",
            "📸 Vintage 1800s Photography": "vintage_1800s_photography",
            "👴 Vintage Anthropomorphic": "vintage_anthropomorphic",
            "🎨 Watercolor": "watercolor",
        }
        self.theme_mappings = emoji_mappings
    
    def get_handler(self, theme: str) -> Optional[BaseThemeHandler]:
        """Get a theme handler by its internal name."""
        return self.handlers.get(theme)
    
    def get_internal_theme(self, display_theme: str) -> str:
        """Get internal theme name from display name."""
        return self.theme_mappings.get(display_theme, "random")
    
    def get_random_theme(self) -> str:
        """Get a random theme name, excluding 'random'."""
        available_themes = [k for k in self.handlers.keys() if k != "random"]
        if not available_themes:
            raise ValueError("No theme handlers available")
        return self.config_manager.random.choice(available_themes)
    
    def get_all_display_themes(self) -> List[str]:
        """Get all theme display names."""
        return list(self.theme_mappings.keys())

class IsulionMegaPromptV3:
    """
    Enhanced version of the Mega Prompt Generator with improved organization and features.
    - vintage_1800s_photography: Authentic 1800s photography style with period-correct processes and effects
    """
    
    TITLE = "🚀 Mega Prompt V3"
    
    def __init__(self):
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize theme registry
        self.theme_registry = ThemeRegistry(self.config_manager)
        
        # Initialize theme mappings
        self.theme_mappings = self.theme_registry.theme_mappings
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """Define input types for the node."""
        # Create a temporary registry to get theme names
        temp_registry = ThemeRegistry(ConfigManager())
        return {
            "required": {
                "theme": (temp_registry.get_all_display_themes(), {"default": "🎲 Dynamic Random"}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
                "debug_mode": (["off", "on"], {"default": "off"}),
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
                include_effects: str = "yes", debug_mode: str = "off") -> Tuple[str, str, str, str, str, int]:
        """Generate a prompt based on the given parameters."""
        try:
            # Set seed if randomization is disabled
            if randomize == "disable":
                self.config_manager.set_seed(seed)
            
            # Get internal theme name and handler
            internal_theme = self.theme_registry.get_internal_theme(theme)
            if internal_theme == "random":
                internal_theme = self.theme_registry.get_random_theme()
            
            handler = self.theme_registry.get_handler(internal_theme)
            if not handler:
                raise ValueError(f"No handler found for theme {internal_theme}")
            
            # Set debug mode
            handler.set_debug(debug_mode == "on")
            
            # Generate components
            components = handler.generate(
                custom_subject=custom_subject,
                custom_location=custom_location,
                include_environment=include_environment,
                include_style=include_style,
                include_effects=include_effects
            )
            
            if not isinstance(components, dict):
                raise ValueError(f"Handler {internal_theme} returned invalid components: {components}")
            
            # Check for required components
            if "subject" not in components:
                raise ValueError(f"Handler {internal_theme} did not generate a subject")
            
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
            error_msg = f"Error generating prompt: {str(e)}"
            print(error_msg)
            return (
                f"Error: {error_msg}",
                "Error in subject generation",
                "Error in environment generation",
                "Error in style generation",
                "Error in effect generation",
                seed
            )
