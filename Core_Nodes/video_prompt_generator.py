import json
import random
import os
from .mega_prompt_V3 import IsulionMegaPromptV3

# Must be the exact same name as used in registration
class IsulionVideoPromptGenerator:
    """Video prompt generator node for ComfyUI"""
    
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), 
                                      "configs", "video_prompt_config.json")
        self.load_config()
        self.mega_prompt = IsulionMegaPromptV3()
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define input types for the node."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 
                                      "configs", "video_prompt_config.json")
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config for INPUT_TYPES: {e}")
            config = {
                "camera_angles": ["The camera remains stationary"],
                "lighting_conditions": ["with natural lighting"],
                "presets": {},
                "quality_modifiers": {
                    "Standard": "professional quality",
                    "High Quality": "high quality",
                    "Best Quality": "best quality"
                }
            }

        # Initialize MegaPromptV3 for themes
        try:
            mega = IsulionMegaPromptV3()
            theme_list = ["None", "🎲 Dynamic Random"] + [k for k in mega.theme_mappings.keys() 
                    if k not in ["None", "🎲 Dynamic Random"]]
        except Exception as e:
            print(f"Error loading themes: {e}")
            theme_list = ["None", "🎲 Dynamic Random"]

        # Prepare input lists
        camera_angles = ["None", "Random"] + config.get("camera_angles", [])
        lighting_conditions = ["None", "Random"] + config.get("lighting_conditions", [])
        presets = ["None"] + [k for k in config.get("presets", {}).keys() if k != "None"]
        quality_levels = list(config.get("quality_modifiers", {}).keys())

        return {
            "required": {
                "preset": (presets, {
                    "default": "None",
                    "display": "📽️ Preset Scenario",
                    "description": "Pre-configured video scenarios with professional settings"
                }),
                "seed": ("INT", {
                    "default": 0, 
                    "min": 0, 
                    "max": 0xffffffffffffffff
                }),
                "quality_level": (quality_levels, {
                    "default": "Standard"
                }),
                "custom_subject": ("STRING", {
                    "default": ""
                }),
                "custom_location": ("STRING", {
                    "default": ""
                }),
                "camera_angle": (camera_angles, {
                    "default": "None"
                }),
                "lighting": (lighting_conditions, {
                    "default": "None"
                }),
                "theme": (theme_list, {
                    "default": "None"
                })
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
                "lighting_conditions": ["with natural lighting"],
                "quality_modifiers": {
                    "Standard": "professional quality",
                    "High Quality": "high quality",
                    "Best Quality": "best quality"
                }
            }

    def generate_prompt(self, preset, seed, quality_level, custom_subject, custom_location, camera_angle, lighting, theme):
        rng = random.Random(seed)
        components = []

        # Add quality modifier first
        if quality_level in self.config.get("quality_modifiers", {}):
            components.append(self.config["quality_modifiers"][quality_level])

        # Handle preset scenarios
        if preset != "None":
            preset_text = self.config.get("presets", {}).get(preset, "")
            if preset_text:
                # Add custom elements if provided
                if custom_subject:
                    preset_text = f"{custom_subject}, {preset_text}"
                if custom_location:
                    preset_text = f"{preset_text} {custom_location}"
                components.append(preset_text)

                # Add camera movement
                if camera_angle != "None":
                    camera = rng.choice(self.config["camera_angles"]) if camera_angle == "Random" else camera_angle
                    if not camera.startswith("(("):
                        camera = f"(({camera}))"
                    components.append(camera)

                # Add lighting
                if lighting != "None":
                    light = rng.choice(self.config["lighting_conditions"]) if lighting == "Random" else lighting
                    components.append(light)

                # Add theme if selected
                if theme != "None" and theme in self.mega_prompt.theme_mappings:
                    theme_key = self.mega_prompt.theme_mappings[theme]
                    handler = self.mega_prompt.theme_registry.handlers.get(theme_key)
                    if handler:
                        theme_components = handler.generate(
                            custom_subject="",
                            custom_location="",
                            include_style="yes",
                            include_effects="yes"
                        )
                        if theme_components and "style" in theme_components:
                            components.append(theme_components["style"])

                # Format and return preset-based prompt
                final_prompt = ", ".join(components)
                if not final_prompt.endswith("."):
                    final_prompt += "."
                return (final_prompt,)

        # Handle custom prompt generation (when no preset is selected)
        subject = custom_subject if custom_subject else rng.choice(self.config["subjects"])
        location = custom_location if custom_location else rng.choice(self.config["locations"])
        components.append(f"{subject} {location}")

        # Add camera movement for custom prompt
        if camera_angle != "None":
            camera = rng.choice(self.config["camera_angles"]) if camera_angle == "Random" else camera_angle
            if not camera.startswith("(("):
                camera = f"(({camera}))"
            components.append(camera)

        # Add lighting for custom prompt
        if lighting != "None":
            light = rng.choice(self.config["lighting_conditions"]) if lighting == "Random" else lighting
            components.append(light)

        # Add theme for custom prompt
        if theme != "None" and theme in self.mega_prompt.theme_mappings:
            theme_key = self.mega_prompt.theme_mappings[theme]
            handler = self.mega_prompt.theme_registry.handlers.get(theme_key)
            if handler:
                theme_components = handler.generate(
                    custom_subject="",
                    custom_location="",
                    include_style="yes",
                    include_effects="yes"
                )
                if theme_components and "style" in theme_components:
                    components.append(theme_components["style"])

        # Format final prompt
        final_prompt = ", ".join(components)
        if not final_prompt.endswith("."):
            final_prompt += "."
        
        return (final_prompt,)

# Update node registration - Use exact class name
NODE_CLASS_MAPPINGS = {
    "IsulionVideoPromptGenerator": IsulionVideoPromptGenerator
}

# Update display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "IsulionVideoPromptGenerator": "Isulion Video Prompt Generator 🎥"
}
