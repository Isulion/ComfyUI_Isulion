import random
from .base_handler import BaseThemeHandler
from typing import Dict

class DisneyThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("disney")

    def _safe_choice(self, key: str, default: str) -> str:
        """Safely choose a random item from a config list with a default fallback."""
        items = self.theme_config.get(key, [])
        result = random.choice(items) if items else default
        self.debug_print(f"[DEBUG] {self.__class__.__name__} - Selected {key}: {result} (from {len(items)} options)")
        return result

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and character features
        style = self._safe_choice("styles", "default style")
        character_feature = self._safe_choice("character_features", "default feature")
        
        # Magical elements and props
        magic = self._safe_choice("magical_elements", "default magic")
        prop = self._safe_choice("props", "default prop")
        
        # Environment and architecture
        environment = self._safe_choice("environments", "default environment") if not location else location
        architecture = self._safe_choice("architectural_elements", "default architecture")
        
        # Lighting and atmosphere
        lighting = self._safe_choice("lighting", "default lighting")
        atmosphere = self._safe_choice("atmospheres", "default atmosphere")
        
        # Color and emotion
        color_scheme = self._safe_choice("color_schemes", "default color scheme")
        emotional_tone = self._safe_choice("emotional_tones", "default emotional tone")
        
        # Animation effect and character type
        animation_effect = self._safe_choice("animation_effects", "default animation effect")
        character_type = self._safe_choice("character_types", "default character type")
        
        # Build the prompt
        prompt_parts = []
        
        # Add subject if provided
        if subject:
            prompt_parts.append(f"((masterful portrait of {subject}))")
        else:
            prompt_parts.append(f"((masterful portrait of {character_type}))")
        
        # Add character details
        prompt_parts.extend([
            f"((with {character_feature}))",
            f"((in {style} style))",
            f"((holding {prop}))",
            f"((with {magic} magical effects))"
        ])
        
        # Add environment if location provided
        if location:
            prompt_parts.append(f"((in {location}))")
        else:
            prompt_parts.append(f"((in {environment}))")
        
        # Add architectural elements
        prompt_parts.append(f"((with {architecture}))")
        
        # Add atmosphere and lighting
        prompt_parts.extend([
            f"((in {atmosphere} atmosphere))",
            f"((with {lighting} lighting))",
            f"((in {color_scheme} colors))",
            f"((showing {emotional_tone} emotion))",
            f"((with {animation_effect} animation style))"
        ])
        
        # Join all parts
        prompt = ", ".join(prompt_parts)
        
        # Add quality tags
        quality_tags = [
            "((Disney animation style))",
            "((masterful artwork))",
            "((perfect composition))",
            "((highly detailed))",
            "((professional quality))",
            "((magical atmosphere))"
        ]
        
        return f"{prompt}, {', '.join(quality_tags)}"

    def get_negative_prompt(self):
        return "low quality, blurry, distorted, deformed, ugly, amateur, unprofessional, non-Disney style"

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Disney-themed components with magical and whimsical elements."""
        self.debug_print(f"\n[DEBUG] {self.__class__.__name__} - Generating new prompt...")
        components = {}
        
        # Generate subject
        subject = custom_subject if custom_subject else "character"  # Default to generic character if no custom subject
        style = self._safe_choice("styles", "default style")
        character_feature = self._safe_choice("character_features", "default feature")
        magic = self._safe_choice("magical_elements", "default magic")
        prop = self._safe_choice("props", "default prop")
        emotional_tone = self._safe_choice("emotional_tones", "default emotional tone")
        
        components["subject"] = (
            f"((masterful Disney style portrait)) of {subject}, {character_feature}, "
            f"((with {magic})), ((holding {prop})), "
            f"((in {style})), ((perfect character design)), "
            f"((Disney animation excellence)), ((magical quality)), "
            f"(({emotional_tone} expression))"
        )
        
        # Add environment if requested
        if include_environment == "yes":
            environment = custom_location if custom_location else self._safe_choice("environments", "default environment")
            architecture = self._safe_choice("architectural_elements", "default architecture")
            atmosphere = self._safe_choice("atmospheres", "default atmosphere")
            
            components["environment"] = (
                f"in ((detailed {environment})) with ((detailed {architecture})), "
                f"((perfect Disney environment)), (({atmosphere})), "
                f"((masterful background)), ((perfect composition))"
            )
        
        # Add style elements if requested
        if include_style == "yes":
            lighting = self._safe_choice("lighting", "default lighting")
            color_scheme = self._safe_choice("color_schemes", "default color scheme")
            
            components["style"] = (
                f"((Disney animation style)), ((perfect {lighting})), "
                f"((beautiful {color_scheme})), "
                f"((high detail)), ((professional quality))"
            )
        
        # Add effects if requested
        if include_effects == "yes":
            magic_effect = self._safe_choice("magical_elements", "default magic")
            atmosphere = self._safe_choice("atmospheres", "default atmosphere")
            components["effects"] = (
                f"((magical {magic_effect})), (({atmosphere})), "
                f"((Disney magic)), ((perfect rendering))"
            )
        
        # Add negative prompt
        components["negative"] = ", ".join([
            "deformed", "distorted", "unrealistic anatomy",
            "bad proportions", "low quality", "blurry",
            "amateur", "poorly drawn", "bad art",
            "non-Disney style", "dark themes", "horror elements"
        ])
        
        return components
