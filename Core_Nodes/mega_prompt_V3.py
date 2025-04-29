import random
import os
from typing import Dict, List, Tuple, Optional

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

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.handlers: Dict[str, BaseThemeHandler] = {} # This will store instances
        self.theme_mappings: Dict[str, str] = {}
        self._init_handlers()
        self._init_mappings()

    def _init_handlers(self):
        """Initialize handler instances from globally available classes."""
        # We iterate through the string map and try to get the actual class object
        # from the global scope (where from .theme_handlers import * would place them).
        self.handlers = {}
        for internal_name, class_name_str in HANDLER_CLASS_NAMES_MAP.items():
            # Check if the class name exists in the global scope
            handler_class = globals().get(class_name_str)

            if handler_class is None:
                # The class wasn't imported successfully (likely due to the '*'' import failing for it)
                # print(f"Warning: Handler class '{class_name_str}' for theme '{internal_name}' not found in global scope. Skipping.") # Debugging
                continue # Skip if the class is not available

            # Optional: Add check if it inherits from BaseThemeHandler if BaseThemeHandler import succeeded
            if 'BaseThemeHandler' in globals() and not issubclass(handler_class, BaseThemeHandler):
                 print(f"Warning: Loaded object '{class_name_str}' for theme '{internal_name}' is not a valid handler class (doesn't inherit BaseThemeHandler). Skipping.")
                 continue

            try:
                # Instantiate the class
                self.handlers[internal_name] = handler_class(self.config_manager)
                # print(f"Initialized handler instance for '{internal_name}'") # Debugging
            except Exception as e:
                 # Catch errors during handler initialization
                 print(f"Warning: Error initializing handler '{class_name_str}' for theme '{internal_name}': {e}. Skipping.")
                 continue

        # print(f"Initialized handler instances: {list(self.handlers.keys())}") # Debugging


    def _init_mappings(self):
        """Initialize theme mappings with emojis, filtering based on available handlers."""
        # Define all possible mappings (copied from your original code)
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

        # Filter mappings to only include themes for which handlers were successfully initialized instances
        # Always include the "random" option mapping
        available_internal_names = set(self.handlers.keys()).union({"random"})

        self.theme_mappings = {
            display_name: internal_name
            for display_name, internal_name in all_emoji_mappings.items()
            if internal_name in available_internal_names
        }
        # print(f"Available themes in mappings: {list(self.theme_mappings.keys())}") # Debugging


    def get_handler(self, theme: str) -> Optional[BaseThemeHandler]:
        """Get a theme handler instance by its internal name."""
        return self.handlers.get(theme)

    def get_internal_theme(self, display_theme: str) -> str:
        """Get internal theme name from display name."""
        # Fallback logic moved to generate method for consistency
        # This method just does the lookup. Return 'random' if not found in mappings.
        internal_name = self.theme_mappings.get(display_theme)
        if internal_name is None:
             print(f"Warning: Display theme '{display_theme}' not found in available mappings. Using 'random'.")
             return "random"
        return internal_name


    def get_random_theme(self) -> str:
        """Get a random theme name from available handler instances."""
        available_themes = list(self.handlers.keys()) # self.handlers only contains valid, non-random themes instances
        if not available_themes:
            print("Error: No theme handler instances available for random selection.")
            # Return a fallback theme if 'essential_realistic' exists, otherwise raise error
            if "essential_realistic" in self.handlers:
                 print("Falling back to 'essential_realistic'.")
                 return "essential_realistic"
            else:
                raise ValueError("Cannot select random theme: No handler instances were initialized and no fallback available.")

        return self.config_manager.random.choice(available_themes)

    def get_all_display_themes(self) -> List[str]:
        available_display_themes = list(self.theme_mappings.keys())

        dynamic_random = "🎲 Dynamic Random"

    # Separate 'Dynamic Random' to ensure it's always first
        if dynamic_random in available_display_themes:
            available_display_themes.remove(dynamic_random)

            # Sort the remaining list using a key function that extracts the theme name
            # The lambda function splits the string by the first space (' ', 1) and takes the second part ([-1]).
            # .strip() removes any leading/trailing whitespace just in case.
            available_display_themes.sort(key=lambda item: item.split(' ', 1)[-1].strip())

            # Insert 'Dynamic Random' back at the beginning
            available_display_themes.insert(0, dynamic_random)
        else:
            # If 'Dynamic Random' isn't there, just sort the whole list by theme name
            available_display_themes.sort(key=lambda item: item.split(' ', 1)[-1].strip())
        return available_display_themes



class IsulionMegaPromptV3:
    """
    Enhanced version of the Mega Prompt Generator with improved organization and features.
    Includes dynamic theme selection, custom inputs, and LoRA key option.
    """

    TITLE = "🚀 Mega Prompt V3"

    def __init__(self):
        # Initialize configuration manager
        self.config_manager = ConfigManager()

        # Initialize theme registry. This will attempt to load and instantiate handlers.
        self.theme_registry = ThemeRegistry(self.config_manager)

        # ** FIX: Expose theme_mappings directly on the node instance **
        # This addresses the AttributeError reported by ComfyUI during loading/initialization
        self.theme_mappings = self.theme_registry.theme_mappings

        # Optional: Check if any handlers were successfully loaded for actual generation
        if not self.theme_registry.handlers and "random" not in self.theme_registry.theme_mappings.values():
             print("CRITICAL WARNING: No theme handler instances were successfully loaded and 'random' option is unavailable. The node will likely fail to generate prompts.")


    @classmethod
    def INPUT_TYPES(cls) -> Dict:
        """Define input types for the node."""
        # Use a temporary registry just to get theme names for the dropdown.
        # It reflects the handlers loaded during the main module import process.
        # Use a fresh ConfigManager for this temp instance to avoid side effects if possible.
        # NOTE: If ConfigManager initialization has side effects, you might reuse self.config_manager
        # from the class instance somehow, but this is tricky in a @classmethod.
        # Using a new instance is standard for INPUT_TYPES.
        # IMPORTANT: If the error 'IsulionMegaPromptV3' object has no attribute 'theme_mappings'
        # *still* occurs after the fix in __init__, it might be because ComfyUI accesses
        # theme_mappings during the static INPUT_TYPES phase *before* __init__ is called
        # on an instance. If so, a dummy placeholder `theme_mappings = {}` might be
        # needed at the class level, but try the fix in __init__ first.
        temp_registry = ThemeRegistry(ConfigManager())
        available_themes = temp_registry.get_all_display_themes()

        # Provide a fallback default if no themes are available at all
        default_theme = "🎲 Dynamic Random" if "🎲 Dynamic Random" in available_themes else (available_themes[0] if available_themes else "--- Error ---")

        # Handle the case where no themes loaded - prevent empty dropdown
        if not available_themes:
             available_themes = ["--- Error ---"]
             default_theme = "--- Error ---"
             print("Error: No themes available for INPUT_TYPES dropdown.")

        return {
            "required": {
                "theme": (available_themes, {"default": default_theme}),
                "complexity": (["simple", "detailed", "complex"], {"default": "detailed"}), # Complexity unused in generate?
                "randomize": (["enable", "disable"], {"default": "enable"}),
                "debug_mode": (["off", "on"], {"default": "off"}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "custom_location": ("STRING", {"default": "", "multiline": True}),
                "lora_key": ("STRING", {"default": "", "multiline": True}), # LORA KEY INPUT
                "include_environment": (["yes", "no"], {"default": "yes"}),
                "include_style": (["yes", "no"], {"default": "yes"}),
                "include_effects": (["yes", "no"], {"default": "yes"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "subject", "environment", "style", "effects", "seed")
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, theme: str, complexity: str = "detailed", randomize: str = "enable", # Complexity unused?
                seed: int = 0, custom_subject: str = "", custom_location: str = "",
                lora_key: str = "", # LORA KEY PARAMETER
                include_environment: str = "yes", include_style: str = "yes",
                include_effects: str = "yes", debug_mode: str = "off") -> Tuple[str, str, str, str, str, int]:
        """Generate a prompt based on the given parameters."""
        # The 'seed' parameter is the actual seed ComfyUI provides (random or fixed)
        return_seed = seed

        # Handle the case where INPUT_TYPES might have defaulted to the error message string
        if theme == "--- Error ---":
             error_msg = "Prompt generation failed: Theme handlers could not be loaded during startup."
             print(error_msg)
             return (error_msg, "", "", "", "", return_seed) # Return empty strings for components

        try:
            # Set the seed for the internal random instance.
            self.config_manager.set_seed(seed)

            # Get internal theme name from display name
            # get_internal_theme now returns 'random' if display name not found
            internal_theme = self.theme_registry.get_internal_theme(theme)

            # If the internal theme is 'random', pick a random one from available handlers
            if internal_theme == "random":
                try:
                    # get_random_theme will raise ValueError if no handlers loaded (except fallback)
                    internal_theme = self.theme_registry.get_random_theme()
                except ValueError as e:
                    error_msg = f"Error selecting random theme: {e}"
                    print(error_msg)
                    return (
                        f"Error: {error_msg}",
                        "", "", "", "", # Empty component strings
                        return_seed
                    )


            handler = self.theme_registry.get_handler(internal_theme)

            # This check is vital: did we actually get a handler instance?
            if not handler:
                 # This case should be rare if get_internal_theme and get_random_theme work correctly
                 error_msg = f"Error: Handler instance for theme '{internal_theme}' (selected via '{theme}') could not be found or was not initialized."
                 print(error_msg)
                 return (
                    error_msg, "", "", "", "", return_seed # Empty component strings
                 )


            # Set debug mode for the handler
            handler.set_debug(debug_mode == "on")

            # Generate components using the handler
            # Pass boolean flags for include options
            components = handler.generate(
                custom_subject=custom_subject,
                custom_location=custom_location,
                # lora_key is handled later
                include_environment=(include_environment == "yes"),
                include_style=(include_style == "yes"),
                include_effects=(include_effects == "yes")
                # Pass complexity if handlers use it: complexity=complexity
            )

            # Ensure handler returned a dictionary
            if not isinstance(components, dict):
                raise TypeError(f"Handler for theme '{internal_theme}' returned invalid type: {type(components)}. Expected dict.")

            # Build a list of prompt parts
            prompt_parts = []
            subject = components.get("subject", "")
            if subject and isinstance(subject, str):
                prompt_parts.append(subject)
            elif subject is not None: # Only warn if subject was *something* but not a string
                 print(f"Warning: Handler for theme '{internal_theme}' generated subject of type {type(subject)}. Expected string.")


            if include_environment == "yes":
                environment = components.get("environment", "")
                if isinstance(environment, str):
                    if environment:
                        prompt_parts.append(environment)
                else:
                    print(f"Warning: Handler for theme '{internal_theme}' generated environment of type {type(environment)}. Expected string.")


            if include_style == "yes":
                style = components.get("style", "")
                if isinstance(style, str):
                    if style:
                        prompt_parts.append(style)
                else:
                    print(f"Warning: Handler for theme '{internal_theme}' generated style of type {type(style)}. Expected string.")


            if include_effects == "yes":
                effects = components.get("effects", "")
                if isinstance(effects, str):
                    if effects:
                        prompt_parts.append(effects)
                else:
                    print(f"Warning: Handler for theme '{internal_theme}' generated effects of type {type(effects)}. Expected string.")


            # Add the Lora Key if provided and not empty
            if lora_key and lora_key.strip():
                 prompt_parts.append(lora_key.strip())

            # Join non-empty parts
            final_prompt = ", ".join(filter(None, prompt_parts))

            # Return the generated components and the seed used
            # Ensure outputs are always strings, even if handler returned something else or keys were missing
            return (
                final_prompt,
                components.get("subject", "") if isinstance(components.get("subject"), str) else "",
                components.get("environment", "") if include_environment == "yes" and isinstance(components.get("environment"), str) else "",
                components.get("style", "") if include_style == "yes" and isinstance(components.get("style"), str) else "",
                components.get("effects", "") if include_effects == "yes" and isinstance(components.get("effects"), str) else "",
                return_seed
            )

        except Exception as e:
            # Catch any other exceptions during generation
            error_msg = f"Error during prompt generation for theme '{theme}' (internal '{internal_theme if 'internal_theme' in locals() else 'N/A'}'): {type(e).__name__}: {str(e)}"
            print(error_msg)
            return (
                f"Error: {error_msg}",
                "", "", "", "", # Return empty strings for components on error
                return_seed
            )