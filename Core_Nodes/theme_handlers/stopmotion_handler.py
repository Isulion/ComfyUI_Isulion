import random
from .base_handler import BaseThemeHandler
from typing import Dict

class StopMotionThemeHandler(BaseThemeHandler):
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("stopmotion")

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and material textures
        style = random.choice(self.theme_config.get("styles", []))
        texture = random.choice(self.theme_config.get("material_textures", []))
        
        # Character features and props
        character_feature = random.choice(self.theme_config.get("character_features", []))
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
        
        # Add subject with stop-motion context
        if subject:
            if any(word in subject.lower() for word in ["person", "man", "woman", "character"]):
                prompt_parts.extend([
                    f"{subject} as a {character_type}",
                    f"with {character_feature}"
                ])
            else:
                prompt_parts.extend([
                    f"handcrafted {subject}",
                    f"with {texture}"
                ])
        
        # Add environment and architecture
        prompt_parts.extend([
            f"in a {environment}",
            f"with {architecture}"
        ])
        
        # Add props and lighting
        prompt_parts.extend([
            f"featuring {prop}",
            f"illuminated by {lighting}"
        ])
        
        # Add atmosphere and emotion
        prompt_parts.extend([
            f"with {atmosphere}",
            f"creating a {emotional_tone} feeling"
        ])
        
        # Add material texture and color scheme
        prompt_parts.extend([
            f"showing {texture}",
            f"in {color_scheme}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "smooth 3D, CGI, digital animation, realistic textures, photorealistic, modern rendering, perfect surfaces, high detail, sharp edges, digital effects"

    def _safe_choice(self, key: str, default: str) -> str:
        """Safely choose a random item from a config list with a default fallback."""
        items = self.theme_config.get(key, [])
        result = random.choice(items) if items else default
        self.debug_print(f"[DEBUG] {self.__class__.__name__} - Selected {key}: {result} (from {len(items)} options)")
        return result

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate stop-motion themed components."""
        self.debug_print("Generating new prompt...")
        components = {}

        # Generate subject
        if custom_subject:
            base_character = custom_subject
        else:
            base_character = self._safe_choice("character_types", "character")
            
        self.debug_print(f"Selected base character: {base_character}")
        
        # Add character features
        material = self._safe_choice("materials", "clay")
        texture = self._safe_choice("textures", "textured")
        detail = self._safe_choice("details", "intricate")
        
        self.debug_print(f"Selected material: {material}")
        self.debug_print(f"Selected texture: {texture}")
        self.debug_print(f"Selected detail: {detail}")
        
        # Generate pose and expression
        pose = self._safe_choice("poses", "dynamic pose")
        expression = self._safe_choice("expressions", "expressive")
        
        self.debug_print(f"Selected pose: {pose}")
        self.debug_print(f"Selected expression: {expression}")
        
        # Combine character elements
        components["subject"] = (
            f"((masterful stop-motion)) of {base_character}, made of {material}, "
            f"with {texture} texture, {detail} details, in {pose}, "
            f"with {expression} expression, ((perfect character design)), "
            f"((highly detailed))"
        )
        
        # Add environment if requested
        if include_environment:
            if custom_location:
                setting = custom_location
            else:
                setting = self._safe_choice("settings", "miniature set")
            
            self.debug_print(f"Selected setting: {setting}")
            
            prop = self._safe_choice("props", "handcrafted prop")
            atmosphere = self._safe_choice("atmospheres", "atmospheric")
            
            self.debug_print(f"Selected prop: {prop}")
            self.debug_print(f"Selected atmosphere: {atmosphere}")
            
            components["environment"] = (
                f"in ((detailed {setting})) with {prop}, "
                f"((with {atmosphere} atmosphere)), ((perfect set design))"
            )
        
        # Add style elements if requested
        if include_style:
            art_style = self._safe_choice("art_styles", "stop-motion animation")
            lighting = self._safe_choice("lighting_styles", "dramatic lighting")
            color_palette = self._safe_choice("color_palettes", "rich colors")
            
            self.debug_print(f"Selected art style: {art_style}")
            self.debug_print(f"Selected lighting: {lighting}")
            self.debug_print(f"Selected color palette: {color_palette}")
            
            components["style"] = (
                f"((masterful {art_style})), ((perfect {lighting})), "
                f"((beautiful {color_palette})), ((professional quality)), "
                f"((perfect composition))"
            )
        
        # Add effects if requested
        if include_effects:
            special_effect = self._safe_choice("special_effects", "practical effect")
            technique = self._safe_choice("techniques", "stop-motion technique")
            
            self.debug_print(f"Selected special effect: {special_effect}")
            self.debug_print(f"Selected technique: {technique}")
            
            components["effects"] = (
                f"((dramatic {special_effect})), ((masterful {technique})), "
                f"((stop-motion excellence)), ((perfect craftsmanship))"
            )
        
        # Add negative prompt
        components["negative"] = ", ".join([
            "3D animation", "CGI", "digital art", "smooth texture",
            "low quality", "blurry", "distorted", "deformed",
            "bad art", "amateur", "poorly crafted"
        ])
        
        return components
