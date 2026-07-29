import random
import os
from typing import Dict, List, Tuple, Optional
import json

# Config imports
try:
    from .configs.config_manager import ConfigManager
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import ConfigManager from '.configs.config_manager': {e}")
    class ConfigManager:
        def __init__(self):
            print("Warning: Using dummy ConfigManager. Node will not function correctly.")
            self.random = random
        def set_seed(self, seed):
            print(f"Warning: Dummy ConfigManager: set_seed called with {seed}")
            self.random.seed(seed)
        def get_current_seed(self):
            print("Warning: Dummy ConfigManager: get_current_seed called.")
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


# Import base handler
try:
    from .theme_handlers.base_handler import BaseThemeHandler
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import BaseThemeHandler: {e}")
    class BaseThemeHandler:
        def __init__(self, config_manager=None):
            self.config_manager = config_manager or ConfigManager()
            self.debug = False
        def set_debug(self, debug: bool):
            self.debug = debug
        def generate(self, custom_subject: str, custom_location: str, include_environment: bool, include_style: bool, include_effects: bool) -> Dict[str, str]:
            print("Warning: Using dummy BaseThemeHandler. Prompt generation will be empty.")
            return {"subject": "Error: Dummy handler used", "environment": "", "style": "", "effects": ""}


# Import theme handler registry (declarative registration)
try:
    from .theme_handlers.registry import (
        get_handler_instance,
        list_handlers,
        get_registered_names,
        clear_instance_cache,
    )
    print("[MegaPromptV3] Theme handler registry loaded successfully.")
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import theme handler registry: {e}")
    def get_handler_instance(name, config): return None
    def list_handlers(): return {}
    def get_registered_names(): return []
    def clear_instance_cache(): pass


# Emoji to internal name mappings (display name -> internal name)
# This replaces the old HANDLER_CLASS_NAMES_MAP and all_emoji_mappings
THEME_DISPLAY_MAP: Dict[str, str] = {
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
    "🌆 Cyberpunk": "cyberpunk",
    "🍳 Culinary/Food": "culinary_food",
    "👗 Curvy Fashion": "curvy_fashion",
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
    "🏛️ Spartan 300": "s300",
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
}


class ThemeRegistry:
    """Registry for managing theme handlers with lazy instantiation."""

    def __init__(self, config_manager: ConfigManager, debug: bool = False):
        self.config_manager = config_manager
        self.debug = debug
        # Lazy: handlers instantiated on first access via get_handler()
        self._handler_instances: Dict[str, BaseThemeHandler] = {}
        self._build_theme_mappings()

    def _debug_print(self, msg: str):
        if self.debug:
            print(msg)

    def _build_theme_mappings(self):
        """Build display_name -> internal_name mapping for available handlers."""
        registered = set(get_registered_names())
        # Always include "random" as a virtual theme
        available = registered | {"random"}

        self.theme_mappings = {
            display_name: internal_name
            for display_name, internal_name in THEME_DISPLAY_MAP.items()
            if internal_name in available
        }
        self._debug_print(f"[ThemeRegistry] Built mappings: {list(self.theme_mappings.keys())}")

    def get_handler(self, theme: str) -> Optional[BaseThemeHandler]:
        """Get handler instance, creating it lazily on first access."""
        if theme in self._handler_instances:
            return self._handler_instances[theme]

        handler = get_handler_instance(theme, self.config_manager)
        if handler:
            self._handler_instances[theme] = handler
            self._debug_print(f"[ThemeRegistry] Lazy-instantiated handler for '{theme}'")
        else:
            self._debug_print(f"[ThemeRegistry] No handler found for '{theme}'")
        return handler

    def get_internal_theme(self, display_theme: str) -> str:
        """Convert display theme name to internal name."""
        internal = self.theme_mappings.get(display_theme)
        if internal is None:
            print(f"Warning: Display theme '{display_theme}' not found. Using 'random'.")
            return "random"
        return internal

    def get_random_theme(self) -> str:
        """Pick a random available theme (excluding 'random')."""
        available = [name for name in self.theme_mappings.values() if name != "random"]
        if not available:
            if "essential_realistic" in self.theme_mappings.values():
                print("Falling back to 'essential_realistic'.")
                return "essential_realistic"
            raise ValueError("No theme handlers available for random selection.")
        return self.config_manager.random.choice(available)

    def get_all_display_themes(self) -> List[str]:
        """Get sorted list of display themes for UI dropdown."""
        themes = list(self.theme_mappings.keys())
        # Sort alphabetically by name (ignoring emoji), keep "Dynamic Random" first
        dynamic_random = "🎲 Dynamic Random"
        if dynamic_random in themes:
            themes.remove(dynamic_random)
            themes.sort(key=lambda x: x.split(' ', 1)[-1].strip())
            themes.insert(0, dynamic_random)
        else:
            themes.sort(key=lambda x: x.split(' ', 1)[-1].strip())
        return themes


def deduplicate_prompt_parts(parts: List[str]) -> List[str]:
    """Remove duplicate prompt parts while preserving order (case-insensitive)."""
    seen = set()
    result = []
    for part in parts:
        norm = part.strip().lower()
        if norm and norm not in seen:
            seen.add(norm)
            result.append(part)
    return result


class IsulionMegaPromptV3:
    """Mega Prompt Generator V3 with lazy-loaded theme handlers and cached UI themes."""

    # Class-level cache for INPUT_TYPES dropdown (computed once)
    _cached_themes: Optional[List[str]] = None
    _cached_theme_registry: Optional[ThemeRegistry] = None

    TITLE = "🚀 Mega Prompt V3"

    def __init__(self):
        try:
            self.debug_mode = False
            self.config_manager = ConfigManager()
            # Reuse cached registry if available, else create new
            if IsulionMegaPromptV3._cached_theme_registry is not None:
                self.theme_registry = IsulionMegaPromptV3._cached_theme_registry
                self.config_manager = self.theme_registry.config_manager
            else:
                self.theme_registry = ThemeRegistry(self.config_manager, debug=self.debug_mode)
                IsulionMegaPromptV3._cached_theme_registry = self.theme_registry
            self.theme_mappings = self.theme_registry.theme_mappings
            if self.debug_mode:
                print(f"[DEBUG] Instance theme_mappings: {list(self.theme_mappings.keys())}")
            if not self.theme_registry.theme_mappings:
                print("CRITICAL WARNING: No theme handlers loaded. Node will fail.")
        except Exception as e:
            print(f"[ERROR] IsulionMegaPromptV3.__init__ failed: {type(e).__name__}: {e}")
            self.theme_mappings = {}
            self.theme_registry = None

    @classmethod
    def _get_cached_themes(cls) -> List[str]:
        """Get cached theme list for INPUT_TYPES, computing once."""
        if cls._cached_themes is None:
            try:
                # Create a temporary registry just for theme discovery
                temp_config = ConfigManager()
                temp_registry = ThemeRegistry(temp_config, debug=False)
                cls._cached_themes = temp_registry.get_all_display_themes()
                cls._cached_theme_registry = temp_registry
                print(f"[MegaPromptV3] Cached {len(cls._cached_themes)} themes for UI dropdown")
            except Exception as e:
                print(f"[ERROR] Failed to cache themes: {type(e).__name__}: {e}")
                cls._cached_themes = ["--- Error ---"]
        return cls._cached_themes

    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        themes = cls._get_cached_themes()
        default = "🎲 Dynamic Random" if "🎲 Dynamic Random" in themes else (themes[0] if themes else "--- Error ---")
        if not themes:
            themes = ["--- Error ---"]
            default = "--- Error ---"
            print("Error: No themes available for INPUT_TYPES dropdown.")
        return {
            "required": {
                "theme": (themes, {"default": default}),
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
            print(f"[DEBUG] generate called: theme={theme}, seed={seed}")
        return_seed = seed

        if theme == "--- Error ---":
            error_msg = "Prompt generation failed: Theme handlers could not be loaded."
            print(error_msg)
            return (error_msg, theme, "", "", "", "", return_seed)

        try:
            self.config_manager.set_seed(seed)

            internal_theme = self.theme_registry.get_internal_theme(theme)
            selected_theme_display = theme

            if internal_theme == "random":
                try:
                    internal_theme = self.theme_registry.get_random_theme()
                    # Find display name for the random theme
                    for display_name, internal_name in self.theme_registry.theme_mappings.items():
                        if internal_name == internal_theme:
                            selected_theme_display = display_name
                            break
                    else:
                        selected_theme_display = internal_theme
                except ValueError as e:
                    error_msg = f"Error selecting random theme: {e}"
                    print(error_msg)
                    return (f"Error: {error_msg}", "random", "", "", "", "", return_seed)
            else:
                for display_name, internal_name in self.theme_registry.theme_mappings.items():
                    if internal_name == internal_theme:
                        selected_theme_display = display_name
                        break

            handler = self.theme_registry.get_handler(internal_theme)
            if self.debug_mode:
                print(f"[DEBUG] Got handler for '{internal_theme}': {handler}")

            if not handler:
                error_msg = f"Error: Handler for theme '{internal_theme}' (via '{theme}') not found or failed to initialize."
                print(error_msg)
                return (error_msg, selected_theme_display, "", "", "", "", return_seed)

            handler.set_debug(debug_mode == "on")

            components = handler.generate(
                custom_subject=custom_subject,
                custom_location=custom_location,
                include_environment=(include_environment == "yes"),
                include_style=(include_style == "yes"),
                include_effects=(include_effects == "yes"),
            )
            if self.debug_mode:
                print(f"[DEBUG] Handler returned: {components}")

            if not isinstance(components, dict):
                raise TypeError(f"Handler for '{internal_theme}' returned {type(components)}, expected dict.")

            prompt_parts = []
            subject = components.get("subject", "")
            if subject and isinstance(subject, str):
                prompt_parts.append(subject)

            if include_environment == "yes":
                env = components.get("environment", "")
                if isinstance(env, str) and env:
                    prompt_parts.append(env)

            if include_style == "yes":
                style = components.get("style", "")
                if isinstance(style, str) and style:
                    prompt_parts.append(style)

            if include_effects == "yes":
                effects = components.get("effects", "")
                if isinstance(effects, str) and effects:
                    prompt_parts.append(effects)

            if lora_key and lora_key.strip():
                prompt_parts.append(lora_key.strip())

            prompt_parts = deduplicate_prompt_parts(prompt_parts)
            final_prompt = ", ".join(filter(None, prompt_parts))

            return (
                final_prompt,
                selected_theme_display,
                components.get("subject", "") if isinstance(components.get("subject"), str) else "",
                components.get("environment", "") if include_environment == "yes" and isinstance(components.get("environment"), str) else "",
                components.get("style", "") if include_style == "yes" and isinstance(components.get("style"), str) else "",
                components.get("effects", "") if include_effects == "yes" and isinstance(components.get("effects"), str) else "",
                return_seed
            )

        except (Exception,) as e:
            error_msg = f"Error during prompt generation for theme '{theme}' (internal '{internal_theme if 'internal_theme' in locals() else 'N/A'}'): {type(e).__name__}: {str(e)}"
            print(error_msg)
            return (
                f"Error: {error_msg}",
                theme,
                "", "", "", "",
                return_seed
            )