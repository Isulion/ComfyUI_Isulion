import random
import os
from typing import Dict, List, Tuple, Optional
import json

# Config imports - Reverting to the original import that you said was working
# This suggests that ComfyUI's loading context makes '.configs' resolve correctly.
try:
    from .configs.config_manager import ConfigManager
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import ConfigManager from '.configs.config_manager'. Please check the file path and your __init__.py. Error: {e}")
    # Define a dummy ConfigManager to prevent immediate crash, but node won't work.
    class ConfigManager:
        def __init__(self):
            print("Warning: Using dummy ConfigManager. Node will not function correctly.")
            self.random = random # Fallback to standard random, won't be seeded by ComfyUI
        def set_seed(self, seed):
             print(f"Warning: Dummy ConfigManager: set_seed called with {seed}")
             self.random.seed(seed)
        def get_current_seed(self):
             print("Warning: Dummy ConfigManager: get_current_seed called.")
             # Standard random doesn't expose current state easily, return dummy
             return 0
        def _load_configs(self):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"[DEBUG] ConfigManager._load_configs: current_dir={current_dir}")
            self.configs = {}
            found_json = False
            for filename in os.listdir(current_dir):
                if filename.endswith('.json'):
                    found_json = True
                    file_path = os.path.join(current_dir, filename)
                    print(f"[DEBUG] Loading config file: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.configs.update(json.load(f))
                    except Exception as e:
                        print(f"[ERROR] Error loading config file {filename}: {str(e)}")
            if not found_json:
                print("[WARNING] No .json config files found in config directory!")
            if not self.configs:
                print("[WARNING] No configs loaded in ConfigManager!")


# Import the base handler class.
# Based on your tree, this should be in theme_handlers/base_handler.py
# This was missing from the original snippet you provided, causing the NameError.
try:
    from .theme_handlers.base_handler import BaseThemeHandler
    # print("Successfully imported BaseThemeHandler") # Debugging
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import BaseThemeHandler from '.theme_handlers.base_handler'. Ensure the file exists and defines BaseThemeHandler. Error: {e}")
    # Define a dummy BaseThemeHandler to allow the node to load, but generation will fail.
    class BaseThemeHandler:
        def __init__(self, config_manager=None):
            self.config_manager = config_manager or ConfigManager() # Use dummy ConfigManager if needed
            self.debug = False
        def set_debug(self, debug: bool):
            self.debug = debug
        def generate(self, custom_subject: str, custom_location: str, include_environment: bool, include_style: bool, include_effects: bool) -> Dict[str, str]:
            print("Warning: Using dummy BaseThemeHandler. Prompt generation will be empty.")
            return {"subject": "Error: Dummy handler used", "environment": "", "style": "", "effects": ""}


# Import all theme handlers using the original pattern.
# This relies on your theme_handlers/__init__.py or directory structure
# correctly exposing the handler classes.
# This *might* be the source of the 'NameError' if the __init__py isn't right,
# but let's stick to the original structure first.
try:
    # This import needs to make classes like AbstractThemeHandler, etc., available in the local scope
    from .theme_handlers import *
    print("Successfully imported theme handlers via '*'.") # Debugging
except ImportError as e:
    print(f"CRITICAL WARNING: Could not import theme handlers using 'from .theme_handlers import *'. Theme selection may be limited or fail. Error: {e}")
    # Continue loading, but warn the user. ThemeRegistry will have limited or no handlers.


# Now define the mapping from display name to internal name.
# We *must* use the class names here as strings, because the 'from ... import *'
# happens *before* this dictionary is defined, making the class names available.
# But the dictionary needs the *names*, not the classes themselves directly for lookup.
# We rely on ThemeRegistry._init_handlers to check if the class exists *after* import *.
HANDLER_CLASS_NAMES_MAP = {
    # Using strings for class names now
    "abstract": "AbstractThemeHandler",
    "animation_cartoon": "AnimationCartoonThemeHandler",
    "anime": "AnimeThemeHandler",
    "architectural": "ArchitecturalThemeHandler",
    "bio_organic_tech": "BioOrganicTechThemeHandler",
    "binet_surreal": "BinetSurrealThemeHandler",
    "caricature": "CaricatureThemeHandler",
    "chimera_animals": "ChimeraAnimalsThemeHandler",
    "chimera_cute_animals": "ChimeraCuteAnimalsThemeHandler",
    "christmas": "ChristmasThemeHandler",
    "cinema_studio": "CinemaStudioThemeHandler",
    "clay_art": "ClayArtThemeHandler",
    "comic_book": "ComicBookThemeHandler",
    "character_designer": "CharacterDesignerThemeHandler",
    "chinese_new_year": "ChineseNewYearThemeHandler",
    "concept_art": "ConceptArtThemeHandler",
    "crayon_art": "CrayonArtThemeHandler",
    "crystalpunk": "CrystalpunkThemeHandler",
    "cyberpunk": "CyberpunkThemeHandler",
    "culinary_food": "CulinaryFoodThemeHandler",
    "curvy_fashion": "CurvyFashionThemeHandler",
    "dia_de_los_muertos": "DiaDeLosmuertosThemeHandler",
    "digital_art": "DigitalArtThemeHandler",
    "disney": "DisneyThemeHandler",
    "dreamworks": "DreamworksThemeHandler",
    "dimension_3d": "Dimension3DThemeHandler",
    "easter": "EasterThemeHandler",
    "enchanted_fantasy": "EnchantedFantasyThemeHandler",
    "essential_realistic": "EssentialRealisticThemeHandler",
    "essential_vintage": "EssentialVintageThemeHandler",
    "ethereal_dreams": "EtherealDreamsThemeHandler",
    "experimental_art": "ExperimentalArtThemeHandler",
    "fantasy": "FantasyThemeHandler",
    "fifties_commercial": "FiftiesCommercialHandler",
    "futuristic_battlefield": "FuturisticBattlefieldThemeHandler",
    "futuristic_city": "FuturisticCityThemeHandler",
    "futuristic_city_metropolis": "FuturisticCityMetropolisThemeHandler",
    "futuristic_scifi": "FuturisticSciFiThemeHandler",
    "ghibli": "GhibliThemeHandler",
    "halloween": "HalloweenThemeHandler",
    "halloween_ethereal": "HalloweenEtherealThemeHandler",
    "historical_monuments": "HistoricalMonumentsHandler",
    "horror": "HorrorThemeHandler",
    "impressionist": "ImpressionistThemeHandler",
    "instagram": "InstagramThemeHandler",
    "instagram_lifestyle": "InstagramLifestyleThemeHandler",
    "interior_spaces": "InteriorSpacesThemeHandler",
    "logo": "LogoThemeHandler",
    "manga_panel": "MangaPanelThemeHandler",
    "marvel": "MarvelThemeHandler",
    "medieval": "MedievalThemeHandler",
    "microscopic": "MicroscopicThemeHandler",
    "minimalist": "MinimalistThemeHandler",
    "miura": "MiuraThemeHandler",
    "nature": "NatureThemeHandler",
    "new_years_eve": "NewYearsEveThemeHandler",
    "nolan": "NolanThemeHandler",
    "peaky_blinders": "PeakyBlindersThemeHandler",
    "pixar": "PixarThemeHandler",
    "post_apocalyptic": "PostApocalypticThemeHandler",
    "puzzle_dimension": "PuzzleDimensionHandler", # Corrected? Original had puzzle_dimension, tree has puzzle_dimension_handler
    "scifi": "SciFiThemeHandler",
    "school_manga": "SchoolMangaThemeHandler",
    "selfie": "SelfieThemeHandler",
    "skinny_blonde_girl": "SkinnyBlondeGirlHandler",
    "Spartan_300": "s300ThemeHandler",
    "spectral_mist": "SpectralMistThemeHandler",
    "st_patricks_day": "StPatricksDayThemeHandler",
    "star_wars": "StarWarsThemeHandler",
    "steampunk": "SteampunkThemeHandler",
    "stopmotion": "StopMotionHandler", # Corrected? Original had stopmotion, tree has stopmotion_handler
    "street_food_kebab": "StreetFoodKebabThemeHandler",
    "thanksgiving": "ThanksgivingThemeHandler",
    "underwater_civilization": "UnderwaterCivilizationThemeHandler",
    "urban_tag": "UrbanTagThemeHandler",
    "valentines_day": "ValentinesDayThemeHandler",
    "village_world": "VillageWorldThemeHandler",
    "vintage_1800s_photography": "Vintage1800sPhotographyHandler",
    "vintage_anthropomorphic": "VintageAnthropomorphicThemeHandler",
    "watercolor": "WatercolorThemeHandler",
    # Removed duplicates that were in your original list
}


class ThemeRegistry:
    """Registry for managing theme handlers and their mappings."""

    def __init__(self, config_manager: ConfigManager, debug: bool = False):
        self.config_manager = config_manager
        self.debug = debug
        self.handlers: Dict[str, BaseThemeHandler] = {}
        self.theme_mappings: Dict[str, str] = {}
        self._init_handlers()
        self._init_mappings()

    def _debug_print(self, msg):
        if self.debug:
            print(msg)

    def _init_handlers(self):
        self._debug_print("[DEBUG] ThemeRegistry._init_handlers called")
        self.handlers = {}
        for internal_name, class_name_str in HANDLER_CLASS_NAMES_MAP.items():
            handler_class = globals().get(class_name_str)
            if handler_class is None:
                self._debug_print(f"[DEBUG] Handler class '{class_name_str}' for theme '{internal_name}' not found in global scope.")
                continue
            if 'BaseThemeHandler' in globals() and not issubclass(handler_class, BaseThemeHandler):
                print(f"Warning: Loaded object '{class_name_str}' for theme '{internal_name}' is not a valid handler class (doesn't inherit BaseThemeHandler). Skipping.")
                continue
            try:
                self.handlers[internal_name] = handler_class(self.config_manager)
                self._debug_print(f"[DEBUG] Initialized handler for '{internal_name}' ({class_name_str})")
            except Exception as e:
                print(f"Warning: Error initializing handler '{class_name_str}' for theme '{internal_name}': {e}. Skipping.")
                continue
        if not self.handlers:
            print("[WARNING] No theme handlers were initialized in ThemeRegistry!")

    def _init_mappings(self):
        self._debug_print("[DEBUG] ThemeRegistry._init_mappings called")
        all_emoji_mappings = {
            "🎲 Dynamic Random": "random",
            "🎨 Abstract": "abstract",
            "📺 Animation Cartoon": "animation_cartoon",
            "🎌 Anime": "anime",
            "🏛️ Architectural": "architectural",
            "🖼️ Binet Surreal": "binet_surreal",
            "🧬 Bio-Organic Technology": "bio_organic_tech",
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
            "🖼️ Digital Art": "digital_art",
            "💠 Dimension 3D": "dimension_3d",
            "🎡 Disney": "disney",
            "🎬 Dreamworks": "dreamworks",
            "🐰 Easter": "easter",
            "✨ Enchanted Fantasy": "enchanted_fantasy",
            "📸 Essential Realistic": "essential_realistic",
            "🕰️ Essential Vintage": "essential_vintage",
            "✨ Ethereal Dreams": "ethereal_dreams",
            "🔬 Experimental Art": "experimental_art",
            "⚔️ Fantasy": "fantasy",
            "🧺 50s Commercial": "fifties_commercial",
            "⚔️ Futuristic Battlefield": "futuristic_battlefield",
            "🌆 Futuristic City": "futuristic_city",
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
            "👧 Skinny Blonde Girl": "skinny_blonde_girl",
            "🏛️ Spartan 300": "Spartan_300",
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
            "🎨 Watercolor": "watercolor"
        }

        available_internal_names = set(self.handlers.keys()).union({"random"})

        self.theme_mappings = {
            display_name: internal_name
            for display_name, internal_name in all_emoji_mappings.items()
            if internal_name in available_internal_names
        }
        self._debug_print(f"[DEBUG] theme_mappings after filtering: {list(self.theme_mappings.keys())}")


    def get_handler(self, theme: str) -> Optional[BaseThemeHandler]:
        return self.handlers.get(theme)

    def get_internal_theme(self, display_theme: str) -> str:
        internal_name = self.theme_mappings.get(display_theme)
        if internal_name is None:
             print(f"Warning: Display theme '{display_theme}' not found in available mappings. Using 'random'.")
             return "random"
        return internal_name


    def get_random_theme(self) -> str:
        available_themes = list(self.handlers.keys())
        if not available_themes:
            print("Error: No theme handler instances available for random selection.")
            if "essential_realistic" in self.handlers:
                 print("Falling back to 'essential_realistic'.")
                 return "essential_realistic"
            else:
                raise ValueError("Cannot select random theme: No handler instances were initialized and no fallback available.")

        return self.config_manager.random.choice(available_themes)

    def get_all_display_themes(self) -> List[str]:
        available_display_themes = list(self.theme_mappings.keys())

        dynamic_random = "🎲 Dynamic Random"

        if dynamic_random in available_display_themes:
            available_display_themes.remove(dynamic_random)

            available_display_themes.sort(key=lambda item: item.split(' ', 1)[-1].strip())

            available_display_themes.insert(0, dynamic_random)
        else:
            available_display_themes.sort(key=lambda item: item.split(' ', 1)[-1].strip())
        return available_display_themes


def deduplicate_prompt_parts(parts):
    """Remove duplicate prompt parts while preserving order and ignoring case/whitespace."""
    seen = set()
    result = []
    for part in parts:
        norm = part.strip().lower()
        if norm and norm not in seen:
            seen.add(norm)
            result.append(part)
    return result


class IsulionMegaPromptV3:
    theme_mappings = {}

    TITLE = "🚀 Mega Prompt V3"

    def __init__(self):
        try:
            self.debug_mode = False
            self.config_manager = ConfigManager()
            self.theme_registry = ThemeRegistry(self.config_manager, debug=self.debug_mode)
            self.theme_mappings = self.theme_registry.theme_mappings
            if self.debug_mode:
                print(f"[DEBUG] theme_mappings set on instance: {list(self.theme_mappings.keys())}")
            if not self.theme_registry.handlers and "random" not in self.theme_registry.theme_mappings.values():
                print("CRITICAL WARNING: No theme handler instances were successfully loaded and 'random' option is unavailable. The node will likely fail to generate prompts.")
        except Exception as e:
            print(f"[ERROR] Exception in IsulionMegaPromptV3.__init__: {type(e).__name__}: {e}")
            self.theme_mappings = {}
            self.theme_registry = None

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        debug_mode = False
        try:
            if debug_mode:
                print("[DEBUG] IsulionMegaPromptV3.INPUT_TYPES called")
            temp_registry = ThemeRegistry(ConfigManager(), debug=debug_mode)
            if debug_mode:
                print(f"[DEBUG] temp_registry.theme_mappings: {list(temp_registry.theme_mappings.keys())}")
            available_themes = temp_registry.get_all_display_themes()
            if debug_mode:
                print(f"[DEBUG] available_themes for dropdown: {available_themes}")
        except Exception as e:
            print(f"[ERROR] Exception in INPUT_TYPES: {type(e).__name__}: {e}")
            available_themes = ["--- Error ---"]
        default_theme = "🎲 Dynamic Random" if "🎲 Dynamic Random" in available_themes else (available_themes[0] if available_themes else "--- Error ---")
        if not available_themes:
            available_themes = ["--- Error ---"]
            default_theme = "--- Error ---"
            print("Error: No themes available for INPUT_TYPES dropdown.")
        return {
            "required": {
                "theme": (available_themes, {"default": default_theme}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
                "debug_mode": (["off", "on"], {"default": "off"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "custom_location": ("STRING", {"default": "", "multiline": True}),
                "lora_key": ("STRING", {"default": "", "multiline": True}),
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
                lora_key: str = "",
                include_environment: str = "yes", include_style: str = "yes",
                include_effects: str = "yes", debug_mode: str = "off") -> Tuple[str, str, str, str, str, int]:
        self.debug_mode = (debug_mode == "on")
        if self.debug_mode:
            print(f"[DEBUG] generate called with theme={theme}, seed={seed}")
        return_seed = seed

        if theme == "--- Error ---":
             error_msg = "Prompt generation failed: Theme handlers could not be loaded during startup."
             print(error_msg)
             return (error_msg, "", "", "", "", return_seed)

        try:
            self.config_manager.set_seed(seed)

            internal_theme = self.theme_registry.get_internal_theme(theme)

            if internal_theme == "random":
                try:
                    internal_theme = self.theme_registry.get_random_theme()
                except ValueError as e:
                    error_msg = f"Error selecting random theme: {e}"
                    print(error_msg)
                    return (
                        f"Error: {error_msg}",
                        "", "", "", "",
                        return_seed
                    )


            handler = self.theme_registry.get_handler(internal_theme)
            if self.debug_mode:
                print(f"[DEBUG] Got handler for internal_theme={internal_theme}: {handler}")

            if not handler:
                 error_msg = f"Error: Handler instance for theme '{internal_theme}' (selected via '{theme}') could not be found or was not initialized."
                 print(error_msg)
                 return (
                    error_msg, "", "", "", "", return_seed
                 )

            handler.set_debug(debug_mode == "on")

            components = handler.generate(
                custom_subject=custom_subject,
                custom_location=custom_location,
                include_environment=(include_environment == "yes"),
                include_style=(include_style == "yes"),
                include_effects=(include_effects == "yes")
            )
            if self.debug_mode:
                print(f"[DEBUG] Handler returned components: {components}")

            if not isinstance(components, dict):
                raise TypeError(f"Handler for theme '{internal_theme}' returned invalid type: {type(components)}. Expected dict.")

            prompt_parts = []
            subject = components.get("subject", "")
            if subject and isinstance(subject, str):
                prompt_parts.append(subject)
            elif subject is not None:
                 print(f"Warning: Handler for theme '{internal_theme}' generated subject of type {type(subject)}. Expected string.")

            if include_environment:
                environment = components.get("environment", "")
                if self.debug_mode:
                    print(f"[DEBUG] environment type: {type(environment)}, value: {environment!r}")
                if isinstance(environment, str):
                    if environment:
                        prompt_parts.append(environment)

            if include_style:
                style = components.get("style", "")
                if self.debug_mode:
                    print(f"[DEBUG] style type: {type(style)}, value: {style!r}")
                if isinstance(style, str):
                    if style:
                        prompt_parts.append(style)

            if include_effects:
                effects = components.get("effects", "")
                if self.debug_mode:
                    print(f"[DEBUG] effects type: {type(effects)}, value: {effects!r}")
                if isinstance(effects, str):
                    if effects:
                        prompt_parts.append(effects)

            if lora_key and lora_key.strip():
                 prompt_parts.append(lora_key.strip())

            # Deduplicate prompt parts globally before joining
            prompt_parts = deduplicate_prompt_parts(prompt_parts)

            final_prompt = ", ".join(filter(None, prompt_parts))

            return (
                final_prompt,
                components.get("subject", "") if isinstance(components.get("subject"), str) else "",
                components.get("environment", "") if include_environment and isinstance(components.get("environment"), str) else "",
                components.get("style", "") if include_style and isinstance(components.get("style"), str) else "",
                components.get("effects", "") if include_effects and isinstance(components.get("effects"), str) else "",
                return_seed
            )

        except Exception as e:
            error_msg = f"Error during prompt generation for theme '{theme}' (internal '{internal_theme if 'internal_theme' in locals() else 'N/A'}'): {type(e).__name__}: {str(e)}"
            print(error_msg)
            return (
                f"Error: {error_msg}",
                "", "", "", "",
                return_seed
            )