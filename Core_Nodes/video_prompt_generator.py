import json
import random
import os
from ..mega_prompt_V3 import MegaPromptV3

class VideoPromptGenerator:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      "configs", "video_prompt_config.json")
        self.load_config()
        self.mega_prompt = MegaPromptV3()
        
        # Create reverse mapping for theme names
        self.theme_name_to_key = {name: key for name, key in self.mega_prompt.theme_mappings.items()}
    
    @classmethod
    def INPUT_TYPES(cls):
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                      "configs", "video_prompt_config.json")
            with open(config_path, 'r') as f:
                config = json.load(f)
                camera_angles = ["Random"] + config["camera_angles"]
                lighting_conditions = ["Random"] + config["lighting_conditions"]
        except Exception as e:
            print(f"Error loading config for INPUT_TYPES: {e}")
            camera_angles = ["Random", "The camera remains stationary"]
            lighting_conditions = ["Random", "with natural lighting"]

        # Add theme selection with emoticons
        themes = ["None"] + sorted([
            "🎌 Anime", "🎨 Abstract", "🚀 Sci-Fi", "💫 Pixar", "⚔️ Fantasy",
            "🌆 Cyberpunk", "🍃 Ghibli", "👻 Horror", "⚙️ Steampunk", "🎨 Watercolor",
            "🎯 Logo", "😄 Caricature", "🌃 Futuristic City", "🎃 Halloween",
            "📱 Instagram", "🦸 Marvel", "🔬 Microscopic", "⬜ Minimalist",
            "📺 Animation Cartoon", "🏛️ Architectural", "🧬 Bio-Organic Technology",
            "🖼️ Binet Surreal", "🦄 Chimera Animals", "🐰 Chimera Cute Animals",
            "🎄 Christmas", "🎬 Cinema Studio", "🏺 Clay Art", "📺 Comic Book",
            "🎨 Concept Art", "🖌️ Crayon Art", "💎 Crystalpunk", "🍳 Culinary/Food",
            "👗 Curvy Fashion", "🖼️ Digital Art", "💠 Dimension 3D", "✨ Enchanted Fantasy",
            "📸 Essential Realistic", "✨ Essential Vintage", "✨ Ethereal Dreams",
            "🔬 Experimental Art", "💥 Futuristic Battlefield", "🌆 Futuristic City Metropolis",
            "🚀 Futuristic Sci-Fi", "👻 Halloween Ethereal", "🎨 Impressionist",
            "📱 Instagram Lifestyle", "📺 Manga Panel", "🕴️‍♂️ Peaky Blinders",
            "🌪️ Post Apocalyptic", "📚 School Manga", "🚀 Star Wars",
            "🌊 Underwater Civilization", "🏙️ Urban Tag", "🏠 Village World",
            "👴 Vintage Anthropomorphic", "📱 Selfie", "🥙 Street Food Kebab",
            "🧩 Puzzle Dimension", "👤 Character Designer", "🎭 Stop Motion",
            "🎡 Disney", "🎬 Dreamworks", "🏠 Interior Spaces", "🐰 Easter",
            "💘 Valentine's Day", "🎆 New Year's Eve", "🦃 Thanksgiving",
            "🍀 St. Patrick's Day", "👹 Dia de los Muertos", "🏮 Chinese New Year"
        ])
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "custom_subject": ("STRING", {"default": "", "multiline": False}),
                "custom_location": ("STRING", {"default": "", "multiline": False}),
                "camera_angle": (camera_angles,),
                "lighting": (lighting_conditions,),
                "theme": (themes,),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Isulion/Prompt"

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {
                "subjects": ["a person"],
                "locations": ["in a room"],
                "camera_angles": ["The camera remains stationary"],
                "lighting_conditions": ["with natural lighting"]
            }

    def generate_prompt(self, seed, custom_subject="", custom_location="", camera_angle="", lighting="", theme="None"):
        # Set random seed for reproducibility
        rng = random.Random(seed)
        
        # Generate base video prompt components
        subject = custom_subject if custom_subject else rng.choice(self.config["subjects"])
        
        # Handle location with proper preposition
        if custom_location:
            # Check if location already starts with a preposition
            prepositions = ["in", "at", "near", "by", "inside", "outside"]
            has_preposition = any(custom_location.lower().startswith(prep) for prep in prepositions)
            location = custom_location if has_preposition else f"in {custom_location}"
        else:
            location = rng.choice(self.config["locations"])
        
        # Handle camera angle and lighting with Random option
        camera = rng.choice(self.config["camera_angles"]) if camera_angle == "Random" else camera_angle
        lighting_condition = rng.choice(self.config["lighting_conditions"]) if lighting == "Random" else lighting

        # Initialize prompt with standard format
        prompt = f"{subject} {location}. "

        # Apply theme if selected
        if theme != "None":
            # Get theme key from the mapping
            theme_key = self.mega_prompt.theme_mappings.get(theme)
            if not theme_key:
                # Try without emoticon if not found
                theme_key = theme.split()[-1].lower().replace("-", "_")
            
            # Get theme handler from mega prompt handlers dictionary
            if theme_key in self.mega_prompt.handlers:
                theme_handler = self.mega_prompt.handlers[theme_key]
                # Generate themed components
                theme_components = theme_handler.generate(
                    custom_subject=subject,
                    custom_location=location,
                    include_environment="yes",
                    include_style="yes",
                    include_effects="yes"
                )
                
                # Only override prompt if we got valid theme components
                if theme_components:
                    prompt = ""
                    if "subject" in theme_components:
                        prompt += theme_components["subject"] + " "
                    if "environment" in theme_components:
                        prompt += theme_components["environment"] + " "
                    if "style" in theme_components:
                        prompt += theme_components["style"] + " "
                    if "effects" in theme_components:
                        prompt += theme_components["effects"] + " "

        # Add cinematic elements to all prompts
        prompt += f"{camera}, capturing the scene as {lighting_condition}. "
        prompt += "The scene unfolds naturally, with fluid movements and authentic expressions. "
        prompt += "The overall composition maintains a cinematic quality with attention to detail and depth."

        return (prompt,)

NODE_CLASS_MAPPINGS = {
    "Isulion Video Prompt Generator 🎥": VideoPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Isulion Video Prompt Generator 🎥": "Isulion Video Prompt Generator 🎥"
}
