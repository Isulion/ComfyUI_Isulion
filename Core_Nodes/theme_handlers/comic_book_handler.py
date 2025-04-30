import random
from typing import Dict
from .base_handler import BaseThemeHandler

class ComicBookThemeHandler(BaseThemeHandler):
    """Handler for comic book-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("comic_book")
        
    def _safe_choice(self, key: str, default: str) -> str:
        """Safely choose a random item from a config list with a default fallback."""
        items = self.theme_config.get(key, [])
        result = random.choice(items) if items else default
        self.debug_print(f"Selected {key}: {result} (from {len(items)} options)")
        return result

    def get_negative_prompt(self) -> str:
        """Generate negative prompt to prevent non-comic styles."""
        return ("photorealistic, photo, realistic, 3d render, cartoon, anime, manga, pixar, "
                "watercolor painting, oil painting, sketch, pencil drawing, crayon, "
                "children's drawing, blurry, out of focus, low quality")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate comic book-themed components."""
        self.debug_print("Generating new comic book prompt...")
        components = {}

        # Generate subject
        if custom_subject:
            base_subject = custom_subject
        else:
            base_subject = self._safe_choice("characters", "superhero")
        
        self.debug_print(f"Selected base subject: {base_subject}")
        
        # Add character features
        pose = self._safe_choice("poses", "dynamic pose")
        feature = self._safe_choice("features", "dramatic costume")
        
        self.debug_print(f"Selected pose: {pose}")
        self.debug_print(f"Selected feature: {feature}")
        
        # Build subject prompt
        components["subject"] = (
            f"((comic book illustration:1.4)), {base_subject}, "
            f"((in {pose}:1.2)), ((with {feature}:1.2)), "
            f"((comic book art:1.3)), ((comic book character:1.3)), "
            f"((bold comic linework:1.2)), ((strong inks:1.2))"
        )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                setting = custom_location
            else:
                setting = self._safe_choice("settings", "dramatic setting")
            
            self.debug_print(f"Selected setting: {setting}")
            
            element = self._safe_choice("elements", "dynamic panel")
            
            self.debug_print(f"Selected element: {element}")
            
            components["environment"] = (
                f"((in dramatic {setting}:1.3)), ((comic book panel:1.4)), "
                f"((with {element}:1.2)), ((comic book background:1.3)), "
                f"((dynamic composition:1.2))"
            )
        
        # Generate style if requested
        if include_style:
            style = self._safe_choice("styles", "classic comic")
            technique = self._safe_choice("techniques", "bold inking")
            
            self.debug_print(f"Selected style: {style}")
            self.debug_print(f"Selected technique: {technique}")
            
            components["style"] = (
                f"((comic book style:1.4)), (({style}:1.3)), "
                f"((with {technique}:1.2)), ((comic book coloring:1.3)), "
                f"((comic book shading:1.2)), ((strong blacks:1.2))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._safe_choice("effects", "dramatic lighting")
            
            self.debug_print(f"Selected effect: {effect}")
            
            components["effects"] = (
                f"((comic book effects:1.3)), ((with {effect}:1.2)), "
                f"((dramatic shadows:1.2)), ((comic book rendering:1.3)), "
                f"((high contrast:1.2))"
            )
        
        return components
