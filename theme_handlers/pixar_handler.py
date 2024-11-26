import random
from typing import Dict
from .base_handler import BaseThemeHandler

class PixarThemeHandler(BaseThemeHandler):
    """Handler for Pixar-style animation themed prompt generation with cinematic quality and storytelling elements."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("pixar")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate sophisticated Pixar-themed components with cinematic quality and emotional depth."""
        components = {}
        
        # Generate subject with enhanced Pixar elements
        if custom_subject:
            components["subject"] = (
                f"((masterfully crafted Pixar-style 3D rendering)) of ((highly detailed {custom_subject})), "
                f"((perfect character design)), ((authentic Pixar aesthetics)), "
                f"((expressive features)), ((charming personality)), "
                f"((perfect character proportions)), ((emotional depth)), "
                f"((cinematic quality)), ((storytelling excellence)), "
                f"((professional 3D animation)), ((Pixar movie quality))"
            )
        else:
            character = self._get_random_choice("pixar.characters")
            emotion = self._get_random_choice("pixar.emotions")
            action = self._get_random_choice("pixar.actions")
            personality = self._get_random_choice("pixar.personalities")
            expression = self._get_random_choice("pixar.expressions")
            components["subject"] = (
                f"((masterfully crafted Pixar-style 3D rendering)) of ((highly detailed {character})), "
                f"((showing {emotion} emotion)), ((dynamically {action})), "
                f"((with {personality} personality)), ((expressing {expression})), "
                f"((perfect character design)), ((authentic Pixar aesthetics)), "
                f"((expressive features)), ((charming personality)), "
                f"((emotional depth)), ((storytelling excellence))"
            )
        
        # Generate environment with enhanced Pixar atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((masterfully crafted Pixar-style {custom_location})), "
                    f"((perfect lighting)), ((rich atmosphere)), "
                    f"((stunning environment detail)), ((authentic Pixar world)), "
                    f"((cinematic composition)), ((emotional storytelling)), "
                    f"((perfect color harmony)), ((dynamic scene)), "
                    f"((professional 3D environment)), ((movie quality))"
                )
            else:
                setting = self._get_random_choice("pixar.settings")
                time = self._get_random_choice("pixar.times")
                weather = self._get_random_choice("pixar.weather")
                atmosphere = self._get_random_choice("pixar.atmospheres")
                lighting = self._get_random_choice("pixar.lighting")
                components["environment"] = (
                    f"in ((masterfully crafted Pixar-style {setting})), "
                    f"((during {weather} {time})), ((in {atmosphere} atmosphere)), "
                    f"((with {lighting})), ((perfect lighting)), ((rich atmosphere)), "
                    f"((stunning environment detail)), ((authentic Pixar world)), "
                    f"((cinematic composition)), ((emotional storytelling))"
                )
        
        # Generate style with enhanced Pixar techniques
        if include_style == "yes":
            style = self._get_random_choice("pixar.styles")
            technique = self._get_random_choice("pixar.techniques")
            color = self._get_random_choice("pixar.color_schemes")
            material = self._get_random_choice("pixar.materials")
            components["style"] = (
                f"((masterful Pixar animation style)), ((professional 3D rendered)), "
                f"((featuring {style})), ((using {technique})), "
                f"((with {color} color scheme)), ((perfect {material} materials)), "
                f"((perfect shading)), ((volumetric lighting)), "
                f"((subsurface scattering)), ((ray tracing)), "
                f"((cinematic composition)), ((emotional depth)), "
                f"((professional color grading)), ((Pixar quality rendering)), "
                f"8k resolution"
            )
        
        # Generate effects with enhanced Pixar elements
        if include_effects == "yes":
            effect = self._get_random_choice("pixar.effects")
            detail = self._get_random_choice("pixar.details")
            particle = self._get_random_choice("pixar.particles")
            ambiance = self._get_random_choice("pixar.ambiance")
            components["effects"] = (
                f"with ((masterful {effect})), ((perfect visual effects)), "
                f"((featuring {detail})), ((with {particle} particles)), "
                f"((in {ambiance} ambiance)), ((emotional depth)), "
                f"((Pixar magic)), ((storytelling excellence)), "
                f"((perfect lighting)), ((cinematic atmosphere)), "
                f"((professional rendering)), ((movie quality))"
            )
        
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
