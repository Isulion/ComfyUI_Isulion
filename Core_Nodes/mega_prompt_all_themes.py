from typing import Dict, List, Tuple, Optional
from .mega_prompt_V3 import IsulionMegaPromptV3

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
            "🍃 Ghibli",
            "🎯 Logo",
            "📚 Manga Panel",
            "🦸 Marvel",
            "🎬 Nolan Epic",
            "💫 Pixar",
            "📚 School Manga",
            "🎭 Stop Motion",
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
            "💻 Digital Art",
            "🔬 Experimental Art",
            "🎨 Impressionist",
            "⬜ Minimalist",
            "🏺 Clay Art",
            "🎨 Watercolor",
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
        ],
        
        "Food": [
            "🍳 Culinary/Food",
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
            "🌿 Nature",
            "🌊 Underwater Civilization",
        ],
        
        "Photography & Fashion": [
            "👗 Curvy Fashion",
            "📸 Essential Realistic",
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
            "💎 Crystalpunk",
            "🌆 Cyberpunk",
            "✨ Enchanted Fantasy",
            "⚔️ Fantasy",
            "⚔️ Futuristic Battlefield",
            "🌃 Futuristic City",
            "🌆 Futuristic City Metropolis",
            "🚀 Futuristic Sci-Fi",
            "⚔️ Miura Dark Fantasy",
            "🚀 Sci-Fi",
            "🚀 Star Wars",
            "⚙️ Steampunk",
            "🌊 Underwater Civilization",
        ],
        
        "Surreal & Dreams": [
            "🖼️ Binet Surreal",
            "💠 Dimension 3D",
            "💫 Ethereal Dreams",
            "🔬 Microscopic",
            "🧩 Puzzle Dimension",
            "💗 Spectral Mist",
        ],
        
        "Vintage & Historical": [
            "🧺 50s Commercial",
            "🕴️‍♂️ Peaky Blinders",
            "🕰️ Essential Vintage",
            "👴 Vintage Anthropomorphic",
            "📸 Vintage 1800s Photography",
        ],
    }
    
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
        
        # Then add all themes sorted by name (ignoring emojis)
        all_sorted_themes = []
        for category in categories:
            all_sorted_themes.extend(cls.theme_categories[category])
        
        # Sort all themes by their names (ignoring emojis)
        all_sorted_themes.sort(key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
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
                })
            },
            "optional": {
                **theme_checkboxes,
                "theme_names": (all_themes, {"default": all_themes[0], "hidden": True})  # Hidden list of all themes with headers
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
            # Get all themes sorted by name
            for category in sorted(self.theme_categories.keys()):
                themes_to_process.extend(self.theme_categories[category])
            
            # Sort by theme name (ignoring emojis)
            themes_to_process.sort(key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
            themes_to_process = list(dict.fromkeys(themes_to_process))  # Remove duplicates while preserving order
        
        # Generate prompts
        positives = []
        names = []
        
        for i, theme in enumerate(themes_to_process):
            try:
                theme_seed = (seed + i) % 0xffffffffffffffff
                
                prompt, subject, env, style, effects, _ = self.mega_prompt.generate(
                    theme=theme,
                    complexity="very detailed",
                    seed=theme_seed,
                    custom_subject=custom_subject,
                    custom_location=custom_location,
                    include_environment="yes",
                    include_style="yes",
                    include_effects="yes",
                    randomize="disable"
                )
                
                if not prompt.startswith("Error:"):
                    positives.append(prompt)
                    names.append(theme)
                
            except Exception as e:
                print(f"Error generating prompt for theme {theme}: {str(e)}")
                continue
        
        return positives, names

class IsulionCategorySelector:
    """Node that selects categories and outputs them for use with the Multiple Prompt Generator."""
    
    def __init__(self):
        self.theme_categories = IsulionMultiplePromptGenerator.theme_categories

    @classmethod
    def INPUT_TYPES(cls):
        # Get list of categories for the combo box
        categories = list(IsulionMultiplePromptGenerator.theme_categories.keys())
        return {
            "required": {
                "selection_mode": (["Single Category", "Multiple Categories"], {"default": "Single Category"}),
                "primary_category": (categories, {"default": categories[0]}),  # Primary category selector
            },
            "optional": {
                **{f"enable_{cat.lower().replace(' & ', '_').replace(' ', '_')}": ("BOOLEAN", {"default": False})
                   for cat in categories}
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_categories",)
    FUNCTION = "select_categories"
    CATEGORY = "Isulion - Multiple Prompt Generator"

    def select_categories(self, selection_mode: str, primary_category: str, **kwargs) -> tuple[str]:
        """Select categories based on primary selection and checkboxes."""
        
        if selection_mode == "Single Category":
            # In single category mode, just return the primary category
            return (primary_category,)
        
        # For multiple categories, combine primary category with checked categories
        selected = [primary_category]  # Always include primary category
        
        # Add any additional checked categories
        for category in self.theme_categories.keys():
            if category != primary_category:  # Skip primary category as it's already included
                checkbox_name = f"enable_{category.lower().replace(' & ', '_').replace(' ', '_')}"
                if kwargs.get(checkbox_name, False):
                    selected.append(category)
        
        # Format the output as a string that can be parsed by the prompt generator
        return ("\n".join(selected),)
