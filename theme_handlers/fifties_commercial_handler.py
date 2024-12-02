import json
import os
import random

from .base_handler import BaseThemeHandler
from typing import Dict

class FiftiesCommercialHandler(BaseThemeHandler):
    """Handler for generating prompts in the style of 1950s commercial advertisements."""
    
    def __init__(self, config_manager):
        """
        Initialize the FiftiesCommercialHandler.
        
        :param config_manager: Configuration manager
        """
        # Call parent's __init__ with config_manager
        super().__init__(config_manager)
        
        # Load configuration from JSON file
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   'configs', 'fifties_commercial_config.json')
        with open(config_path, 'r') as config_file:
            self.theme_config = json.load(config_file)
        
        # Optional: Add theme-specific debug information
        self.debug_print(f"Initialized FiftiesCommercialHandler with {len(self.theme_config.get('subjects', [])) or 0} subjects")

    def get_prompt(self, positive_prompt: str, negative_prompt: str = "") -> Dict[str, str]:
        """Generate a prompt in the style of 1950s commercial advertisements."""
        
        # Get style and visual elements from config
        style_elements = self.theme_config.get('style_elements', [])
        visual_elements = self.theme_config.get('visual_elements', [])
        
        # Combine style elements - now they already contain brackets
        style = ", ".join(random.sample(style_elements, min(2, len(style_elements))))
        visuals = ", ".join(random.sample(visual_elements, min(3, len(visual_elements))))
        
        # Build the complete prompt - the elements already contain their own brackets
        enhanced_prompt = f"{positive_prompt}, {style}, {visuals}"
        
        # Add negative prompt elements specific to 1950s commercial style
        base_negative = self.theme_config.get('negative_prompt_base', 
            "modern elements, contemporary styling, digital artifacts, instagram filters, modern technology")
        enhanced_negative = f"{negative_prompt}, {base_negative}" if negative_prompt else base_negative
        
        return {
            "positive": enhanced_prompt,
            "negative": enhanced_negative
        }

    def get_theme_name(self) -> str:
        """Return the name of the theme."""
        return "50s Commercial"

    def get_theme_description(self) -> str:
        """Return the description of the theme."""
        return "Generate images in the style of 1950s commercial advertisements, featuring vibrant colors, idealized scenes, and classic advertising aesthetics."

    def generate(self, custom_subject: str = "",
            custom_location: str = "",
            include_environment: str = "yes",
            include_style: str = "yes",
            include_effects: str = "yes") -> Dict[str, str]:
        """Generate theme-specific prompts for 1950s commercial style."""
        self.debug_print(f"Theme config: {self.theme_config}")
        
        # If no custom subject is provided, generate a default subject
        if not custom_subject:
            subjects = self.theme_config.get('subjects', [])
            self.debug_print(f"Available subjects: {subjects}")
            
            if not subjects:
                # Fallback if subjects list is empty
                subjects = ["(pristine, gleaming) household appliance", "(innovative, time-saving) kitchen gadget"]
            
            custom_subject = random.choice(subjects)
            self.debug_print(f"Selected subject: {custom_subject}")
        
        # Add location if not specified
        if not custom_location:
            locations = self.theme_config.get('locations', [])
            self.debug_print(f"Available locations: {locations}")
            
            if not locations:
                # Fallback if locations list is empty
                locations = ["(spotless, modern) suburban kitchen", "(sophisticated, spacious) mid-century living room"]
            
            custom_location = random.choice(locations)
            self.debug_print(f"Selected location: {custom_location}")
        
        # Build the positive prompt - now the elements already contain their own descriptive brackets
        positive_prompt = f"{custom_subject} in a {custom_location}"
        
        # Get the prompt details
        prompt_details = self.get_prompt(positive_prompt)
        
        # Return a comprehensive dictionary with all required information
        return {
            "prompt": prompt_details["positive"],
            "subject": custom_subject,
            "environment": custom_location,
            "style": ", ".join(random.sample(self.theme_config.get('style_elements', []), min(2, len(self.theme_config.get('style_elements', []))))),
            "effects": ", ".join(random.sample(self.theme_config.get('visual_elements', []), min(2, len(self.theme_config.get('visual_elements', []))))),
            "seed": random.randint(0, 2**32 - 1)
        }
