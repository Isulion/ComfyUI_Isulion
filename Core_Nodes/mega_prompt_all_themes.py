from typing import Dict, List, Tuple, Optional
import logging

from .mega_prompt_V3 import IsulionMegaPromptV3, available_themes

logger = logging.getLogger(__name__)

class IsulionMultiplePromptGenerator:
    """Node that generates prompts for all available themes using a custom subject and location. """
    
    # Reorganized and sorted theme categories
    theme_categories = {
        "Animation & Entertainment": [
            "🎌 Anime",
            "📺 Animation Cartoon",
            "🎬 Cinema Studio",
            "📚 Comic Book",
            "🎡 Disney",
            "🎬 Dreamworks",
            "🐱 Giant Cat-zilla",
            "🍃 Ghibli",
            "🎯 Logo",
            "📺 Manga Panel",
            "🦸 Marvel",
            "🎬 Nolan Epic",
            "💫 Pixar",
            "👾 16-Bit Pixel Art",
            "📚 School Manga",
            "🎭 Stop Motion",
            "🕹️ Voxel Low-Poly",
        ],
        
        "Architectural & Spaces": [
            "🏛️ Architectural",
            "🏠 Interior Spaces",
            "🏙️ Urban Tag",
            "🏠 Village World",
        ],
        
        "Art Styles & Techniques": [
            "🎨 Abstract",
            "🎨 Concept Art",
            "🖍️ Crayon Art",
            "🖼️ Digital Art",
            "🔬 Experimental Art",
            "🧊 Glassmorphism",
            "🎨 Impressionist",
            "🎈 Inflatable World",
            "🧶 Knitted World",
            "🧊 Liquid Chrome",
            "⬜ Minimalist",
            "🏺 Clay Art",
            "✂️ Papercraft",
            "🎨 Watercolor",
            "🪩 Y2K Retro-Futurism",
        ],
        
        "Character Art": [
            "😄 Caricature",
            "👤 Character Designer",
            "🦄 Chimera Animals",
            "🐰 Chimera Cute Animals",
        ],
        
        "Dark & Horror": [
            "👻 Halloween Ethereal",
            "👻 Horror",
            "⚔️ Miura Dark Fantasy",
            "📹 VHS Found Footage",
        ],
        
        "Food": [
            "🍳 Culinary/Food",
            "🍕 Food Apocalypse",
            "🥙 Street Food Kebab",
        ],
        
        "Holiday Themes": [
            "🏮 Chinese New Year",
            "🎄 Christmas",
            "👹 Dia de los Muertos",
            "🐰 Easter",
            "🎃 Halloween",
            "👻 Halloween Ethereal",
            "🎆 New Year's Eve",
            "🍀 St. Patrick's Day",
            "🦃 Thanksgiving",
            "💘 Valentine's Day",
        ],
        
        "Nature & Environment": [
            "🌌 Astrophotography",
            "🌿 Nature",
            "🌿 Overgrown Ruins",
            "🌊 Underwater Civilization",
        ],
        
        "Photography & Fashion": [
            "🎬 Analog 35mm Film",
            "👗 Curvy Fashion",
            "📸 Essential Realistic",
            "📱 Fisheye Action Cam",
            "📱 Instagram",
            "📱 Instagram Lifestyle",
            "📱 Selfie",
        ],
        
        "Post-Apocalyptic": [
            "🌪️ Post Apocalyptic",
        ],
        
        "Random": [
            "🎲 Dynamic Random"
        ],
        
        "Science Fiction & Fantasy": [
            "🧬 Bio-Organic Technology",
            "🪼 Bioluminescent Jelly",
            "🌧️ Cinematic Neon Rain",
            "💎 Crystalpunk",
            "👟 Cyber Hypebeast",
            "🌆 Cyberpunk",
            "✨ Enchanted Fantasy",
            "⚔️ Fantasy",
            "⚔️ Futuristic Battlefield",
            "🌆 Futuristic City",
            "🌆 Futuristic City Metropolis",
            "🚀 Futuristic Sci-Fi",
            "⚔️ Miura Dark Fantasy",
            "🍄 Psychedelic Cyber Fungus",
            "🚀 Sci-Fi",
            "🚀 Star Wars",
            "⚙️ Steampunk",
            "🌊 Underwater Civilization",
            "🩻 X-Ray Anatomy",
        ],
        
        "Surreal & Dreams": [
            "🖼️ Binet Surreal",
            "💠 Dimension 3D",
            "✨ Ethereal Dreams",
            "🌌 Glitch Core",
            "🛋️ IKEA Backrooms",
            "🔬 Microscopic",
            "🧩 Puzzle Dimension",
            "🦆 Rubber Duck Supremacy",
            "💗 Spectral Mist",
            "📦 Unboxing Surrealism",
        ],
        
        "Vintage & Historical": [
            "🧺 50s Commercial",
            "🪩 Disco Medieval",
            "🕴️ Peaky Blinders",
            "🕰️ Essential Vintage",
            "🛒 Retro Vaporwave Mall",
            "👴 Vintage Anthropomorphic",
            "📸 Vintage 1800s Photography",
            "🏛️ Historical Monuments",
        ],
    }
    
    @classmethod
    def _themes_in_sync_with_registry(cls) -> List[str]:
        """Theme list filtered against the live registry, with drift warnings.

        Keeps stale entries from breaking the UI when handlers are renamed
        or removed: unknown themes are dropped and logged.
        """
        try:
            known = set(available_themes())
        except Exception:
            return [t for themes in cls.theme_categories.values() for t in themes]
        result = []
        for themes in cls.theme_categories.values():
            for theme in themes:
                if theme in known:
                    result.append(theme)
                else:
                    logger.warning("MultiplePromptGenerator: theme '%s' absent du registre (entrée obsolète ignorée).", theme)
        return list(dict.fromkeys(result))  # dédoublonnage stable

    def __init__(self):
        self.mega_prompt = IsulionMegaPromptV3()

    @classmethod
    def INPUT_TYPES(cls):
        # Get all available themes organized by category
        all_themes = []

        # Add all category headers first
        categories = sorted(cls.theme_categories.keys())
        for category in categories:
            all_themes.append(f"[{category}]")

        # Then add all themes sorted by name (ignoring emojis), synced with registry
        all_sorted_themes = sorted(cls._themes_in_sync_with_registry(),
                                   key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
        all_themes.extend(all_sorted_themes)

        # Create checkbox inputs for each theme
        theme_checkboxes = {}
        
        # Add category checkboxes first (sorted)
        for category in categories:
            category_key = f"category_{category.lower().replace(' & ', '_').replace(' ', '_')}"
            theme_checkboxes[category_key] = ("BOOLEAN", {
                "default": False,
                "label": f"Select All {category}"  # Add label for category
            })
        
        # Add all theme checkboxes sorted by name
        for theme in all_sorted_themes:
            # Create key using the full theme name with emoji
            theme_key = theme.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
            theme_checkboxes[theme_key] = ("BOOLEAN", {
                "default": False,
                "label": theme  # Use full theme name as label
            })

        return {
            "required": {
                "selection_mode": (["Theme Selection", "All Themes"], {
                    "default": "Theme Selection"
                }),
                "custom_subject": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "placeholder": "Enter custom subject..."
                }),
                "custom_location": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "placeholder": "Enter custom location..."
                }),
                "seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff
                }),
                "complexity": (["simple", "detailed", "complex"], {
                    "default": "detailed"
                }),
                "include_environment": (["yes", "no"], {"default": "yes"}),
                "include_style": (["yes", "no"], {"default": "yes"}),
                "include_effects": (["yes", "no"], {"default": "yes"}),
                "lora_key": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "(lora:key:weight)..."
                }),
            },
            "optional": {
                **theme_checkboxes,
                "debug_mode": (["off", "on"], {"default": "off"}),
                "theme_names": (all_themes, {"default": all_themes[0], "hidden": True})
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "name")
    FUNCTION = "generate"
    CATEGORY = "Isulion - Multiple Prompt Generator"
    OUTPUT_IS_LIST = (True, True)
    OUTPUT_NODE = True  # Indicates this node has a custom UI

    def get_themes_for_category(self, category: str) -> List[str]:
        """Get list of themes for a specific category."""
        return self.theme_categories.get(category, [])

    def generate(self, 
                selection_mode: str,
                custom_subject: str,
                custom_location: str,
                seed: int,
                complexity: str,
                include_environment: str,
                include_style: str,
                include_effects: str,
                lora_key: str,
                theme_names: List[str],
                **kwargs) -> Tuple[List[str], List[str]]:
        """Generate prompts based on selected themes."""
        
        themes_to_process = []
        
        # Get themes based on selection mode
        if selection_mode == "Theme Selection":
            # Get selected themes from checkboxes
            categories = sorted(self.theme_categories.keys())
            all_themes = []
            
            # Collect all themes
            for category in categories:
                all_themes.extend(self.theme_categories[category])
            
            # Sort all themes by name (ignoring emojis)
            all_themes.sort(key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
            
            # Check category selections
            category_selections = {
                category: kwargs.get(f"category_{category.lower().replace(' & ', '_').replace(' ', '_')}", False)
                for category in categories
            }
            
            # Process themes
            for theme in all_themes:
                # Find which category this theme belongs to
                theme_category = next(
                    category for category in categories 
                    if theme in self.theme_categories[category]
                )
                
                # Create theme key
                theme_key = theme.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                
                # Add theme if its checkbox is checked or if its category is selected
                if category_selections[theme_category] or kwargs.get(theme_key, False):
                    themes_to_process.append(theme)
                    
        elif selection_mode == "All Themes":
            # All known themes, synced with registry and sorted by name
            themes_to_process = self._themes_in_sync_with_registry()
            themes_to_process.sort(key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
        
        # Extract optional params from kwargs
        debug_mode = kwargs.get("debug_mode", "off")

        # Generate prompts
        positives = []
        names = []
        
        for i, theme in enumerate(themes_to_process):
            try:
                theme_seed = (seed + i) % 0xffffffffffffffff
                
                prompt, _, subject, env, style, effects, _ = self.mega_prompt.generate(
                    theme=theme,
                    complexity=complexity,
                    seed=theme_seed,
                    custom_subject=custom_subject,
                    custom_location=custom_location,
                    include_environment=include_environment,
                    include_style=include_style,
                    include_effects=include_effects,
                    lora_key=lora_key,
                    randomize="disable",
                    debug_mode=debug_mode
                )
                
                if not prompt.startswith("Error:"):
                    positives.append(prompt)
                    names.append(theme)
                
            except Exception as e:
                print(f"Error generating prompt for theme {theme}: {str(e)}")
                continue
        
        return positives, names
