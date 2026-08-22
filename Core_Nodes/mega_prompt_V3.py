import random
import os
from functools import lru_cache
from typing import Dict, List, Tuple, Optional

import logging
logger = logging.getLogger(__name__)
import json

# Config imports - Reverting to the original import that you said was working
# This suggests that ComfyUI's loading context makes '.configs' resolve correctly.
try:
    from .configs.config_manager import ConfigManager
except ImportError as e:
    logger.error(f"CRITICAL ERROR: Could not import ConfigManager from '.configs.config_manager'. Please check the file path and your __init__.py. Error: {e}")
    # Define a dummy ConfigManager to prevent immediate crash, but node won't work.
    class ConfigManager:
        def __init__(self):
            logger.warning("Using dummy ConfigManager. Node will not function correctly.")
            self.random = random # Fallback to standard random, won't be seeded by ComfyUI
        def set_seed(self, seed):
             logger.warning(f"Dummy ConfigManager: set_seed called with {seed}")
             self.random.seed(seed)
        def get_current_seed(self):
             logger.warning("Dummy ConfigManager: get_current_seed called.")
             # Standard random doesn't expose current state easily, return dummy
             return 0
        def _load_configs(self):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logger.debug(f"[DEBUG] ConfigManager._load_configs: current_dir={current_dir}")
            self.configs = {}
            found_json = False
            for filename in os.listdir(current_dir):
                if filename.endswith('.json'):
                    found_json = True
                    file_path = os.path.join(current_dir, filename)
                    logger.debug(f"[DEBUG] Loading config file: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.configs.update(json.load(f))
                    except Exception as e:
                        logger.error(f"[ERROR] Error loading config file {filename}: {str(e)}")
            if not found_json:
                logger.warning("[WARNING] No .json config files found in config directory!")
            if not self.configs:
                logger.warning("[WARNING] No configs loaded in ConfigManager!")


# Import the base handler class.
try:
    from .theme_handlers.base_handler import BaseThemeHandler
except ImportError as e:
    logger.error(f"CRITICAL ERROR: Could not import BaseThemeHandler from '.theme_handlers.base_handler'. Ensure the file exists and defines BaseThemeHandler. Error: {e}")
    # Define a dummy BaseThemeHandler to allow the node to load, but generation will fail.
    class BaseThemeHandler:
        def __init__(self, config_manager=None):
            self.config_manager = config_manager or ConfigManager()
            self.debug = False
        def set_debug(self, debug: bool):
            self.debug = debug
        def generate(self, custom_subject: str, custom_location: str, include_environment: bool, include_style: bool, include_effects: bool) -> Dict[str, str]:
            logger.warning("Using dummy BaseThemeHandler. Prompt generation will be empty.")
            return {"subject": "Error: Dummy handler used", "environment": "", "style": "", "effects": ""}


# Decorator-based theme registry: every handler module registers itself at import.
from .theme_handlers.registry import THEME_HANDLERS


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
        for internal_name, handler_class in THEME_HANDLERS.items():
            if not issubclass(handler_class, BaseThemeHandler):
                logger.warning(f"Registered class '{handler_class.__name__}' for theme '{internal_name}' does not inherit BaseThemeHandler. Skipping.")
                continue
            try:
                self.handlers[internal_name] = handler_class(self.config_manager)
                self._debug_print(f"[DEBUG] Initialized handler for '{internal_name}' ({handler_class.__name__})")
            except Exception as e:
                logger.warning(f"Error initializing handler '{handler_class.__name__}' for theme '{internal_name}': {e}. Skipping.")
                continue
        if not self.handlers:
            logger.warning("[WARNING] No theme handlers were initialized in ThemeRegistry!")

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
            "🎨 Watercolor": "watercolor",
            "🧸 Starter Pack": "starter_pack",
            "🚀 Space Colony": "space_colony",
            "🏝️ Tropical Paradise": "tropical_paradise",
            "🧊 Glassmorphism": "glassmorphism",
            "🪩 Y2K Retro-Futurism": "y2k",
            "🎬 Analog 35mm Film": "analog_film",
            "🌌 Astrophotography": "astrophotography",
            "🩻 X-Ray Anatomy": "xray_anatomy",
            "🌧️ Cinematic Neon Rain": "cinematic_neon_rain",
            "✂️ Papercraft": "papercraft",
            "🕹️ Voxel Low-Poly": "voxel",
            "👾 16-Bit Pixel Art": "pixel_art",
            "🌿 Overgrown Ruins": "overgrown_ruins",
            "🐱 Giant Cat-zilla": "giant_cat_zilla",
            "🍕 Food Apocalypse": "food_apocalypse",
            "🪩 Disco Medieval": "disco_medieval",
            "🦆 Rubber Duck Supremacy": "rubber_duck",
            "🎈 Inflatable World": "inflatable_world",
            "🪼 Bioluminescent Jelly": "bioluminescent_jelly",
            "🧶 Knitted World": "knitted_world",
            "🧊 Liquid Chrome": "liquid_chrome",
            "🛋️ IKEA Backrooms": "ikea_backrooms",
            "🌌 Glitch Core": "glitch_core",
            "🍄 Psychedelic Cyber Fungus": "psychedelic_cyber_fungus",
            "📦 Unboxing Surrealism": "unboxing_surrealism",
            "📹 VHS Found Footage": "vhs_found_footage",
            "👟 Cyber Hypebeast": "cyber_hypebeast",
            "🛒 Retro Vaporwave Mall": "retro_vaporwave_mall",
            "📱 Fisheye Action Cam": "fisheye_action_cam"
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
             logger.warning(f"Display theme '{display_theme}' not found in available mappings. Using 'random'.")
             return "random"
        return internal_name


    def get_random_theme(self) -> str:
        available_themes = list(self.handlers.keys())
        if not available_themes:
            logger.error("No theme handler instances available for random selection.")
            if "essential_realistic" in self.handlers:
                 logger.error("Falling back to 'essential_realistic'.")
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


@lru_cache(maxsize=1)
def get_theme_registry() -> "ThemeRegistry":
    """Shared ThemeRegistry singleton.

    Avoids re-reading ~100 JSON config files on every node instantiation or
    INPUT_TYPES call. Themes added/changed on disk require a ComfyUI restart.
    """
    return ThemeRegistry(ConfigManager())


@lru_cache(maxsize=1)
def available_themes() -> List[str]:
    """Cached list of display theme names for dropdowns."""
    return get_theme_registry().get_all_display_themes()


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
            # Shared singleton registry (cheap: no disk I/O after first call)
            self.theme_registry = get_theme_registry()
            self.config_manager = self.theme_registry.config_manager
            self.theme_mappings = self.theme_registry.theme_mappings
            if not self.theme_registry.handlers and "random" not in self.theme_registry.theme_mappings.values():
                logger.warning("CRITICAL WARNING: No theme handler instances were successfully loaded and 'random' option is unavailable. The node will likely fail to generate prompts.")
        except Exception as e:
            logger.error(f"[ERROR] Exception in IsulionMegaPromptV3.__init__: {type(e).__name__}: {e}")
            self.theme_mappings = {}
            self.theme_registry = None

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        debug_mode = False
        try:
            available_themes_list = available_themes()
        except Exception as e:
            logger.error(f"[ERROR] Exception in INPUT_TYPES: {type(e).__name__}: {e}")
            available_themes_list = ["--- Error ---"]
        default_theme = "🎲 Dynamic Random" if "🎲 Dynamic Random" in available_themes_list else (available_themes_list[0] if available_themes_list else "--- Error ---")
        if not available_themes_list:
            available_themes_list = ["--- Error ---"]
            default_theme = "--- Error ---"
            logger.error("No themes available for INPUT_TYPES dropdown.")
        return {
            "required": {
                "theme": (list(available_themes_list), {"default": default_theme}),
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

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "selected_theme", "subject", "environment", "style", "effects", "seed")
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, theme: str, complexity: str = "detailed", randomize: str = "enable",
                seed: int = 0, custom_subject: str = "", custom_location: str = "",
                lora_key: str = "",
                include_environment: str = "yes", include_style: str = "yes",
                include_effects: str = "yes", debug_mode: str = "off") -> Tuple[str, str, str, str, str, str, int]:
        self.debug_mode = (debug_mode == "on")
        if self.debug_mode:
            print(f"[DEBUG] generate called with theme={theme}, seed={seed}")
        return_seed = seed

        if theme == "--- Error ---":
             error_msg = "Prompt generation failed: Theme handlers could not be loaded during startup."
             logger.error(error_msg)
             return (error_msg, theme, "", "", "", "", return_seed)

        try:
            self.config_manager.set_seed(seed)

            internal_theme = self.theme_registry.get_internal_theme(theme)

            # Track the display name of the selected theme for output
            selected_theme_display = theme

            if internal_theme == "random":
                try:
                    internal_theme = self.theme_registry.get_random_theme()
                    # Find the display name for the randomly selected internal theme
                    for display_name, internal_name in self.theme_registry.theme_mappings.items():
                        if internal_name == internal_theme:
                            selected_theme_display = display_name
                            break
                    else:
                        selected_theme_display = internal_theme  # fallback
                except ValueError as e:
                    error_msg = f"Error selecting random theme: {e}"
                    logger.error(error_msg)
                    return (
                        f"Error: {error_msg}",
                        "random",
                        "", "", "", "",
                        return_seed
                    )
            else:
                # Always show the display name for the selected theme
                for display_name, internal_name in self.theme_registry.theme_mappings.items():
                    if internal_name == internal_theme:
                        selected_theme_display = display_name
                        break
                else:
                    selected_theme_display = internal_theme  # fallback

            handler = self.theme_registry.get_handler(internal_theme)
            if self.debug_mode:
                print(f"[DEBUG] Got handler for internal_theme={internal_theme}: {handler}")

            if not handler:
                 error_msg = f"Error: Handler instance for theme '{internal_theme}' (selected via '{theme}') could not be found or was not initialized."
                 logger.error(error_msg)
                 return (
                    error_msg, selected_theme_display, "", "", "", "", return_seed
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
                 logger.warning(f"Handler for theme '{internal_theme}' generated subject of type {type(subject)}. Expected string.")

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
                selected_theme_display,
                components.get("subject", "") if isinstance(components.get("subject"), str) else "",
                components.get("environment", "") if include_environment and isinstance(components.get("environment"), str) else "",
                components.get("style", "") if include_style and isinstance(components.get("style"), str) else "",
                components.get("effects", "") if include_effects and isinstance(components.get("effects"), str) else "",
                return_seed
            )

        except Exception as e:
            error_msg = f"Error during prompt generation for theme '{theme}' (internal '{internal_theme if 'internal_theme' in locals() else 'N/A'}'): {type(e).__name__}: {str(e)}"
            logger.error(error_msg)
            return (
                f"Error: {error_msg}",
                theme,
                "", "", "", "",
                return_seed
            )