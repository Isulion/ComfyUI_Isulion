import random
from typing import Dict
from .base_handler import BaseThemeHandler

class PixarThemeHandler(BaseThemeHandler):
    """Handler for Pixar-style animation themed prompt generation with cinematic quality and storytelling elements."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("pixar")

    def _safe_choice(self, key: str, default: str) -> str:
        """Safely choose a random item from a config list with a default fallback."""
        items = self.theme_config.get(key, [])
        result = random.choice(items) if items else default
        self.debug_print(f"Selected {key}: {result} (from {len(items)} options)")
        return result

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Pixar-themed components."""
        self.debug_print("Generating new prompt...")
        components = {}

        # Generate subject
        if custom_subject:
            base_character = custom_subject
        else:
            base_character = self._safe_choice("character_types", "character")
            
        self.debug_print(f"Selected base character: {base_character}")
        
        # Add character features
        expression = self._safe_choice("expressions", "expressive")
        pose = self._safe_choice("poses", "dynamic pose")
        emotion = self._safe_choice("emotions", "emotional")
        
        self.debug_print(f"Selected expression: {expression}")
        self.debug_print(f"Selected pose: {pose}")
        self.debug_print(f"Selected emotion: {emotion}")
        
        # Generate personality traits
        personality = self._safe_choice("personality_traits", "charming")
        quirk = self._safe_choice("quirks", "unique trait")
        
        self.debug_print(f"Selected personality: {personality}")
        self.debug_print(f"Selected quirk: {quirk}")
        
        # Combine character elements
        components["subject"] = (
            f"((masterful portrait)) of {base_character}, {personality}, "
            f"with {expression} expression, in {pose}, showing {emotion} emotion, "
            f"with {quirk}, ((perfect character design)), ((highly detailed))"
        )
        
        # Add environment if requested
        if include_environment == "yes":
            if custom_location:
                setting = custom_location
            else:
                setting = self._safe_choice("settings", "imaginative setting")
            
            self.debug_print(f"Selected setting: {setting}")
            
            time_of_day = self._safe_choice("times_of_day", "dramatic lighting")
            weather = self._safe_choice("weather_conditions", "atmospheric")
            
            self.debug_print(f"Selected time of day: {time_of_day}")
            self.debug_print(f"Selected weather: {weather}")
            
            components["environment"] = (
                f"in ((detailed {setting})) during {time_of_day}, "
                f"with {weather} conditions, ((perfect environment design))"
            )
        
        # Add style elements if requested
        if include_style == "yes":
            art_style = self._safe_choice("art_styles", "Pixar animation")
            lighting = self._safe_choice("lighting_styles", "dramatic lighting")
            color_palette = self._safe_choice("color_palettes", "vibrant colors")
            
            self.debug_print(f"Selected art style: {art_style}")
            self.debug_print(f"Selected lighting: {lighting}")
            self.debug_print(f"Selected color palette: {color_palette}")
            
            components["style"] = (
                f"((masterful {art_style})), ((perfect {lighting})), "
                f"((beautiful {color_palette})), ((professional quality)), "
                f"((perfect composition))"
            )
        
        # Add effects if requested
        if include_effects == "yes":
            special_effect = self._safe_choice("special_effects", "visual effect")
            atmosphere = self._safe_choice("atmospheres", "atmospheric")
            
            self.debug_print(f"Selected special effect: {special_effect}")
            self.debug_print(f"Selected atmosphere: {atmosphere}")
            
            components["effects"] = (
                f"((dramatic {special_effect})), (({atmosphere})), "
                f"((cinematic quality)), ((perfect rendering))"
            )
        
        # Add negative prompt
        components["negative"] = ", ".join([
            "anime", "manga", "cartoon", "dreamworks style", "disney style",
            "low quality", "blurry", "distorted", "deformed",
            "bad art", "amateur", "poorly drawn"
        ])
        
        return components

    def get_negative_prompt(self):
        """Generate comprehensive negative prompt for Pixar theme."""
        return (
            "((amateur 3D)), ((poor animation)), ((bad lighting)), "
            "((inconsistent style)), ((wrong Pixar elements)), "
            "((non-Pixar aesthetics)), ((poor composition)), "
            "((stiff poses)), ((emotionless)), ((unrealistic effects)), "
            "((wrong perspective)), ((missing details)), "
            "((flat lighting)), ((amateur rendering)), "
            "((weak atmosphere)), ((incorrect materials)), "
            "((poor cinematography)), ((low quality)), "
            "((incorrect scale)), ((missing emotion)), "
            "((blurry)), ((noisy)), ((pixelated)), "
            "((wrong animation style)), ((incorrect rendering)), "
            "((bad special effects)), ((poor character design)), "
            "((incorrect proportions)), ((wrong color schemes)), "
            "realistic, photorealistic, photograph, gritty, dark themes, "
            "scary elements, horror, blood, gore, violent scenes, "
            "adult themes, complex textures, hyper-detailed, ultra-realistic"
        )
