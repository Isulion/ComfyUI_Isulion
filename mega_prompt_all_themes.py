from typing import Dict, List, Tuple, Optional
from .mega_prompt_V3 import MegaPromptV3

class IsulionMultiplePromptGenerator:
    """Node that generates prompts for all available themes using a custom subject and location. """
    
    def __init__(self):
        self.mega_prompt = MegaPromptV3()
        # Define theme categories
        self.theme_categories = {
            "Art Styles & Techniques": [
                "🎨 Abstract",
                "🎨 Concept Art", 
                "🖍️ Crayon Art",
                "💻 Digital Art",
                "🎨 Watercolor", 
                "🏺 Clay Art",
                "⬜ Minimalist",
                "🎨 Impressionist"
            ],
            "Animation & Entertainment": [
                "📺 Animation Cartoon",
                "🎌 Anime", 
                "🎬 Dreamworks",
                "🎡 Disney",
                "🍃 Ghibli", 
                "💫 Pixar",
                "🎭 Stop Motion",
                "📚 Manga Panel", 
                "📚 School Manga",
                "🦸 Marvel"
            ],
            "Science Fiction & Fantasy": [
                "💎 Crystalpunk",
                "🌆 Cyberpunk",
                "🚀 Futuristic Sci-Fi",
                "🌃 Futuristic City",
                "⚔️ Futuristic Battlefield", 
                "🌆 Futuristic City Metropolis",
                "🚀 Sci-Fi",
                "🚀 Star Wars",
                "⚙️ Steampunk",
                "🧬 Bio-Organic Technology",
                "⚔️ Fantasy",
                "✨ Enchanted Fantasy",
                "🌊 Underwater Civilization",
                "⚔️ Miura Dark Fantasy"
            ],
            "Character & Creature Design": [
                "👤 Character Designer",
                "😄 Caricature", 
                "🦄 Chimera Animals",
                "🐰 Chimera Cute Animals"
            ],
            "Environment & Architecture": [
                "🏛️ Architectural",
                "🏠 Interior Spaces", 
                "🏙️ Urban Tag",
                "🏠 Village World"
            ],
            "Special Themes & Occasions": [
                "🎄 Christmas",
                "🎃 Halloween", 
                "👻 Halloween Ethereal",
                "👻 Horror",
                "🐰 Easter",
                "💘 Valentine's Day", 
                "🎆 New Year's Eve",
                "🦃 Thanksgiving", 
                "🍀 St. Patrick's Day",
                "👹 Dia de los Muertos",
                "🏮 Chinese New Year"
            ],
            "Experimental & Unique": [
                "🖼️ Binet Surreal",
                "💫 Ethereal Dreams", 
                "🔬 Experimental Art",
                "🧩 Puzzle Dimension", 
                "💠 Dimension 3D",
                "🔬 Microscopic",
                "🌪️ Post Apocalyptic"
            ],
            "Photography & Social Media": [
                "📸 Essential Realistic",
                "📱 Instagram", 
                "📱 Instagram Lifestyle",
                "📱 Selfie",
                "👗 Curvy Fashion"
            ],
            "Vintage & Historical": [
                "🕰️ Essential Vintage",
                "👴 Vintage Anthropomorphic", 
                "🕴️‍♂️ Peaky Blinders"
            ],
            "Food & Lifestyle": [
                "🍳 Culinary/Food",
                "🥙 Street Food Kebab"
            ],
            "Media & Design": [
                "📚 Comic Book",
                "🎬 Cinema Studio", 
                "🎯 Logo"
            ],
            "Random": [
                "🎲 Dynamic Random"
            ]
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "theme_selection_mode": (["All Themes", "Selected Themes", "Theme Category"], {"default": "All Themes"}),
                "custom_subject": ("STRING", {"default": "", "multiline": True}),
                "custom_location": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "selected_themes": ("STRING", {
                    "multiline": True,
                    "default": "🎨 Abstract\n🎌 Anime\n🌆 Cyberpunk"
                }),
                "theme_category": (["Art Styles & Techniques", "Animation & Entertainment", "Science Fiction & Fantasy", 
                                  "Character & Creature Design", "Environment & Architecture", "Special Themes & Occasions", 
                                  "Experimental & Unique", "Photography & Social Media", "Vintage & Historical", 
                                  "Food & Lifestyle", "Media & Design", "Random"], 
                                  {"default": "Art Styles & Techniques"})
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
        seed: int = 0,
        selected_themes: str = "",
        theme_category: str = "Art Styles & Techniques"
    ) -> Tuple[List[str], List[str]]:
        """Generate prompts for selected themes.
        Returns lists of (positive_prompts, theme_names)"""
        
        # Determine which themes to process based on selection mode
        if theme_selection_mode == "All Themes":
            themes = [theme for theme, internal in self.mega_prompt.theme_mappings.items() 
                     if internal != "random"]
        elif theme_selection_mode == "Selected Themes":
            themes = []
            selected = [theme.strip() for theme in selected_themes.split('\n') if theme.strip()]
            for theme in selected:
                matched = False
                for full_theme in self.mega_prompt.theme_mappings.keys():
                    if theme.strip() in full_theme or full_theme.strip() in theme:
                        themes.append(full_theme)
                        matched = True
                        break
                if not matched:
                    themes.append(theme)
        else:  # Theme Category
            themes = self.theme_categories.get(theme_category, [])
        
        positives = []
        names = []
        
        for i, theme in enumerate(sorted(themes)):
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
                    randomize="disable"  # Always disable randomization
                )
                
                if not prompt.startswith("Error:"):
                    positives.append(prompt)
                    names.append(theme)
                
            except Exception as e:
                print(f"Error generating prompt for theme {theme}: {str(e)}")
                continue
        
        return positives, names
