from typing import Dict, List, Tuple, Optional
from .mega_prompt_V3 import MegaPromptV3

class IsulionMultiplePromptGenerator:
    """Node that generates prompts for all available themes using a custom subject and location. """
    
    def __init__(self):
        self.mega_prompt = MegaPromptV3()
        # Define theme categories
        self.theme_categories = {
            "Art Styles": [
                "🎨 Abstract",
                "🎨 Watercolor",
                "🎨 Impressionist",
                "🖍️ Crayon Art",
                "🏺 Clay Art",
                "🎨 Concept Art",
                "🔬 Experimental Art"
            ],
            "Animation & Comics": [
                "📺 Animation Cartoon",
                "🎌 Anime",
                "📚 Comic Book",
                "🍃 Ghibli",
                "💫 Pixar",
                "🎬 Dreamworks",
                "📺 Manga Panel",
                "📚 School Manga"
            ],
            "Sci-Fi & Future": [
                "🌆 Cyberpunk",
                "🚀 Sci-Fi",
                "🌆 Futuristic City",
                "⚔️ Futuristic Battlefield",
                "🌆 Futuristic City Metropolis",
                "🚀 Futuristic Sci-Fi",
                "🧬 Bio-Organic Technology",
                "💎 Crystalpunk"
            ],
            "Fantasy & Magic": [
                "⚔️ Fantasy",
                "✨ Enchanted Fantasy",
                "✨ Ethereal Dreams",
                "⚔️ Miura Dark Fantasy"
            ],
            "Horror & Spooky": [
                "👻 Horror",
                "🎃 Halloween",
                "👻 Halloween Ethereal"
            ],
            "Holidays": [
                "🎄 Christmas",
                "🐰 Easter",
                "🎆 New Year's Eve",
                "💘 Valentine's Day",
                "🏮 Chinese New Year",
                "👹 Dia de los Muertos",
                "🍀 St. Patrick's Day",
                "🦃 Thanksgiving"
            ],
            "Modern & Lifestyle": [
                "📱 Instagram",
                "📱 Instagram Lifestyle",
                "📱 Selfie",
                "👗 Curvy Fashion",
                "🏠 Interior Spaces",
                "🏙️ Urban Tag"
            ],
            "Character & Design": [
                "😄 Caricature",
                "👤 Character Designer",
                "🦄 Chimera Animals",
                "🐰 Chimera Cute Animals",
                "⬜ Minimalist",
                "🎯 Logo"
            ],
            "Movies & Media": [
                "🎬 Cinema Studio",
                "🎡 Disney",
                "🦸 Marvel",
                "🚀 Star Wars",
                "🎬 Nolan Epic",
                "🕴️‍♂️ Peaky Blinders",
                "🎭 Stop Motion"
            ],
            "Vintage & Historical": [
                "🧺 50s Commercial",
                "🕰️ Essential Vintage",
                "👴 Vintage Anthropomorphic"
            ],
            "Special Effects": [
                "💠 Dimension 3D",
                "🖼️ Digital Art",
                "🧩 Puzzle Dimension",
                "🌊 Underwater Civilization"
            ]
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "theme_selection_mode": (["All Themes", "Selected Themes", "Theme Category"], {"default": "All Themes"}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "custom_location": ("STRING", {"default": "", "multiline": True}),
                "randomize": (["enable", "disable"], {"default": "enable"}),
            },
            "optional": {
                "selected_themes": ("STRING", {
                    "multiline": True,
                    "default": "🎨 Abstract\n🎌 Anime\n🌆 Cyberpunk"
                }),
                "theme_category": (["Art Styles", "Animation & Comics", "Sci-Fi & Future", 
                                  "Fantasy & Magic", "Horror & Spooky", "Holidays", 
                                  "Modern & Lifestyle", "Character & Design", "Movies & Media",
                                  "Vintage & Historical", "Special Effects"], 
                                  {"default": "Art Styles"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive", "name")
    FUNCTION = "generate_all"
    CATEGORY = "Isulion - Multiple Prompt Generator"
    OUTPUT_IS_LIST = (True, True)  # Indicates that each output is a list

    def generate_all(
        self,
        theme_selection_mode: str,
        custom_subject: str = "",
        custom_location: str = "",
        randomize: str = "enable",
        selected_themes: str = "",
        theme_category: str = "Art Styles",
        seed: int = 0
    ) -> Tuple[List[str], List[str]]:
        """Generate prompts for selected themes.
        Returns lists of (positive_prompts, theme_names)"""
        
        # Determine which themes to process based on selection mode
        if theme_selection_mode == "All Themes":
            themes = [theme for theme, internal in self.mega_prompt.theme_mappings.items() 
                     if internal != "random"]
        elif theme_selection_mode == "Selected Themes":
            # Convert selected themes to match theme mappings
            themes = []
            selected = [theme.strip() for theme in selected_themes.split('\n') if theme.strip()]
            for theme in selected:
                # Try to find matching theme with emoji
                matched = False
                for full_theme in self.mega_prompt.theme_mappings.keys():
                    if theme.strip() in full_theme or full_theme.strip() in theme:
                        themes.append(full_theme)
                        matched = True
                        break
                if not matched:
                    themes.append(theme)  # Keep original if no match found
        else:  # Theme Category
            themes = self.theme_categories.get(theme_category, [])
        
        # Store results for each theme
        positives = []
        names = []
        
        # Use provided seed if randomization is disabled
        if randomize == "disable":
            base_seed = seed
        else:
            import random
            base_seed = random.randint(0, 0xffffffffffffffff)
        
        for i, theme in enumerate(sorted(themes)):
            try:
                # Generate prompt for this theme with a unique seed
                theme_seed = (base_seed + i) % 0xffffffffffffffff if randomize == "disable" else 0
                
                prompt, subject, env, style, effects, _ = self.mega_prompt.generate(
                    theme=theme,
                    complexity="very detailed",  # Always set to very detailed
                    randomize=randomize,  # Use the randomize parameter
                    seed=theme_seed,  # Use unique seed for each theme when randomize is disabled
                    custom_subject=custom_subject,
                    custom_location=custom_location,
                    include_environment="yes",
                    include_style="yes",
                    include_effects="yes",
                    debug_mode="off"
                )
                
                # Only add if generation was successful (no error message)
                if not prompt.startswith("Error:"):
                    positives.append(prompt)
                    names.append(theme)
                
            except Exception as e:
                print(f"Error generating prompt for theme {theme}: {str(e)}")
                continue
        
        return positives, names
