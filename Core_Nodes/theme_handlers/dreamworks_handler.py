import random
from .base_handler import BaseThemeHandler
from typing import Dict

class DreamworksThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("dreamworks")

    def _safe_choice(self, key: str, default: str) -> str:
        """Safely choose a random item from a config list with a default fallback."""
        items = self.theme_config.get(key, [])
        result = random.choice(items) if items else default
        self.debug_print(f"[DEBUG] {self.__class__.__name__} - Selected {key}: {result} (from {len(items)} options)")
        return result

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and character features
        style = random.choice(self.theme_config.get("styles", []))
        character_feature = random.choice(self.theme_config.get("character_features", []))
        
        # Visual effects and props
        effect = random.choice(self.theme_config.get("visual_effects", []))
        prop = random.choice(self.theme_config.get("props", []))
        
        # Environment and architecture
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting", []))
        atmosphere = random.choice(self.theme_config.get("atmospheres", []))
        
        # Color and emotion
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        emotional_tone = random.choice(self.theme_config.get("emotional_tones", []))
        
        # Animation effect and character type
        animation_effect = random.choice(self.theme_config.get("animation_effects", []))
        character_type = random.choice(self.theme_config.get("character_types", []))
        
        # Build the prompt
        prompt_parts = []
        
        # Add style and animation effect
        prompt_parts.extend([style, f"with {animation_effect}"])
        
        # Add subject with DreamWorks context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} as a {character_type}",
                    f"with {character_feature}"
                ])
            else:
                prompt_parts.extend([
                    f"epic {subject}",
                    f"enhanced with {effect}"
                ])
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in an {environment}",
            f"featuring {architecture}"
        ])
        
        # Add props and lighting
        prompt_parts.extend([
            f"with {prop}",
            f"illuminated by {lighting}"
        ])
        
        # Add atmosphere and emotion
        prompt_parts.extend([
            f"in an {atmosphere}",
            f"creating a {emotional_tone} feeling"
        ])
        
        # Add visual effects and color scheme
        prompt_parts.extend([
            f"with {effect}",
            f"in {color_scheme}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "anime, hand-drawn, 2D animation, sketchy, traditional animation, low quality, basic rendering, flat colors, simple lighting, undetailed, amateur animation"

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate Dreamworks-themed components."""
        self.debug_print("Generating new prompt...")
        components = {}

        # Always use random elements, even with custom_subject
        base_character = custom_subject if custom_subject else self._safe_choice("character_types", "character")
        expression = self._safe_choice("expressions", "expressive")
        pose = self._safe_choice("poses", "dynamic pose")
        emotion = self._safe_choice("emotions", "emotional")
        personality = self._safe_choice("personality_traits", "charismatic")
        quirk = self._safe_choice("quirks", "unique trait")

        self.debug_print(f"Selected base character: {base_character}")
        self.debug_print(f"Selected expression: {expression}")
        self.debug_print(f"Selected pose: {pose}")
        self.debug_print(f"Selected emotion: {emotion}")
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
            setting = custom_location if custom_location else self._safe_choice("settings", "dramatic setting")
            time_of_day = self._safe_choice("times_of_day", "dramatic lighting")
            weather = self._safe_choice("weather_conditions", "atmospheric")
            self.debug_print(f"Selected setting: {setting}")
            self.debug_print(f"Selected time of day: {time_of_day}")
            self.debug_print(f"Selected weather: {weather}")
            components["environment"] = (
                f"in ((detailed {setting})) during {time_of_day}, "
                f"with {weather} conditions, ((perfect environment design))"
            )

        # Add style elements if requested
        if include_style == "yes":
            art_style = self._safe_choice("art_styles", "Dreamworks animation")
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
            "anime", "manga", "cartoon", "pixar style", "disney style",
            "low quality", "blurry", "distorted", "deformed",
            "bad art", "amateur", "poorly drawn"
        ])

        return components
