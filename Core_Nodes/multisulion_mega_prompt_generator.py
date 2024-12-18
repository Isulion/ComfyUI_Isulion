import random
from typing import Dict, List, Tuple, Optional
from .mega_prompt_V3 import IsulionMegaPromptV3
import comfy.ui

class IsulionMultiplePromptGenerator:
    """Node that generates prompts for all available themes using a custom subject and location."""

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
        ],
        
        "Vintage & Historical": [
            "🧺 50s Commercial",
            "🕴️‍♂️ Peaky Blinders",
            "🕰️ Essential Vintage",
            "👴 Vintage Anthropomorphic",
        ],
    }

    def __init__(self):
        self.mega_prompt = IsulionMegaPromptV3()
        self.category_states = {}  # Track collapse states for categories
        for category in self.theme_categories:
            self.category_states[category] = False # All start collapsed
        self.model_id = None  # Default to None

    @classmethod
    def INPUT_TYPES(cls):
        categories = sorted(cls.theme_categories.keys())
        all_themes = []

        for category in categories:
            all_themes.extend(cls.theme_categories[category])

        all_sorted_themes = sorted(all_themes, key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)

        input_types = {
            "required": {
                "selection_mode": (["Theme Selection", "All Themes", "Selected Categories"], {
                    "default": "Theme Selection"
                }),
                "custom_subject": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "Example: a wizard, a cat, a spaceship"
                }),
                "custom_location": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "placeholder": "Example: a castle, a beach, a city"
                }),
                 "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "filter_text": ("STRING", {"default": "", "label": "Filter Themes"}),
                "model_id": ("STRING", {
                    "default": "",
                    "placeholder": "Enter model ID or leave blank for default"
                }),
            },
            "optional": {},
        }

        for category in categories:
            category_key = f"category_{category.lower().replace(' & ', '_').replace(' ', '_')}"
            input_types["optional"][category_key] = ("BOOLEAN", {
                    "default": False,
                    "label": f"Select All {category}",
                    "tooltip": f"Select all themes in {category}"
             })
    
        for theme in all_sorted_themes:
             theme_key = theme.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
             input_types["optional"][theme_key] = ("BOOLEAN", {
                    "default": False,
                     "label": theme,
                     "tooltip": theme
             })
        input_types["optional"]["theme_names"] = (all_themes, {"default": all_themes[0], "hidden": True})
        input_types["optional"]["seed_randomize"] = ("BUTTON", {"default": False, "label": "Randomize Seed"})

        return input_types

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "name")
    FUNCTION = "generate"
    CATEGORY = "Isulion - Multiple Prompt Generator"
    OUTPUT_IS_LIST = (True, True)
    OUTPUT_NODE = True
    
    def generate(self,
                 selection_mode: str,
                 custom_subject: str,
                 custom_location: str,
                 seed: int,
                 filter_text: str,
                 theme_names: List[str],
                 seed_randomize: bool,
                 model_id: str = None,
                 **kwargs) -> Tuple[List[str], List[str]]:
    
        if seed_randomize:
            seed = random.randint(0, 0xffffffffffffffff)

        themes_to_process = []
        categories = sorted(self.theme_categories.keys())

        # Filter themes based on filter_text if provided
        filter_text = filter_text.lower()

        # Store model ID if provided
        if model_id:
            self.model_id = model_id

        if selection_mode == "Theme Selection":
            for theme in theme_names:
                theme_key = theme.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                if kwargs.get(theme_key, False):
                    if not filter_text or filter_text in theme.lower():
                        themes_to_process.append(theme)

        elif selection_mode == "Selected Categories":
            for category in categories:
                category_key = f"category_{category.lower().replace(' & ', '_').replace(' ', '_')}"
                if kwargs.get(category_key, False):
                    for theme in self.theme_categories[category]:
                        if not filter_text or filter_text in theme.lower():
                            themes_to_process.append(theme)

        elif selection_mode == "All Themes":
            for category in categories:
                for theme in self.theme_categories[category]:
                    if not filter_text or filter_text in theme.lower():
                        themes_to_process.append(theme)

        # Remove duplicates while preserving order
        themes_to_process = list(dict.fromkeys(themes_to_process))
        
        # Sort themes
        themes_to_process.sort(key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)

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

    def update_ui(self):
        categories = sorted(self.theme_categories.keys())
        all_themes = []

        for category in categories:
            all_themes.extend(self.theme_categories[category])

        all_sorted_themes = sorted(all_themes, key=lambda x: x.split(' ', 1)[1] if ' ' in x else x)
        
        ui = []
        ui.append({
            "type": "dropdown",
            "name": "selection_mode",
            "options": ["Theme Selection", "All Themes", "Selected Categories"],
            "label": "Selection Mode"
        })
        ui.append({
            "type": "text",
            "name": "custom_subject",
            "label": "Custom Subject"
        })
        ui.append({
            "type": "text",
            "name": "custom_location",
            "label": "Custom Location"
        })
        ui.append({
            "type": "number",
            "name": "seed",
            "label": "Seed"
        })
        ui.append({
            "type": "button",
            "name": "seed_randomize",
            "text": "Randomize Seed"
        })
        ui.append({
            "type": "text",
            "name": "filter_text",
            "label": "Filter Themes"
        })

        for category in categories:
            category_key = f"category_{category.lower().replace(' & ', '_').replace(' ', '_')}"
            collapsed = self.category_states.get(category, False)
            
            ui.append({
                "type": "button",
                "name": f"{category_key}_toggle",
                "text": f"{'+' if collapsed else '-'} {category}"
            })
            
            if not collapsed:
                ui.append({
                    "type": "checkbox",
                    "name": category_key,
                    "label": category,
                    "default": False
                })
                
                for theme in self.theme_categories[category]:
                    theme_key = theme.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                    ui.append({
                        "type": "checkbox",
                        "name": theme_key,
                        "label": theme,
                        "default": False
                    })

        return ui

    def toggle_category(self, category: str) -> None:
        """Toggle the collapse state of a category"""
        if category in self.category_states:
            self.category_states[category] = not self.category_states[category]