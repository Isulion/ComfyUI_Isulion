import random
from typing import Dict
from .base_handler import BaseThemeHandler

class VillageWorldThemeHandler(BaseThemeHandler):
    """Handler for village of the world-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("village_world")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate village of the world-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((traditional {custom_subject})), "
                f"((village life)), ((cultural)), "
                f"((authentic))"
            )
        else:
            culture = self._get_random_choice("village_world.cultures")
            person = self._get_random_choice("village_world.people")
            activity = self._get_random_choice("village_world.activities")
            components["subject"] = (
                f"((in {culture})), "
                f"(({person})), ((doing {activity})), "
                f"((traditional)), ((cultural))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((traditional {custom_location})) with "
                    f"((village setting)), ((cultural environment))"
                )
            else:
                environment = self._get_random_choice("village_world.environments")
                building = self._get_random_choice("village_world.buildings")
                element = self._get_random_choice("village_world.elements")
                components["environment"] = (
                    f"in (({environment})) with (({building})), "
                    f"((featuring {element})), "
                    f"((village vista)), ((cultural scene))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            atmosphere = self._get_random_choice("village_world.atmospheres")
            components["style"] = (
                f"((styled as {atmosphere})), "
                f"((traditional aesthetic)), "
                f"((village design)), ((cultural look)), "
                f"((authentic atmosphere))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("village_world.effects")
            components["effects"] = (
                f"with (({effect})), "
                f"((village atmosphere)), "
                f"((cultural ambiance)), ((traditional environment))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and atmosphere
        style = random.choice(self.theme_config.get("styles", []))
        atmosphere = random.choice(self.theme_config.get("atmosphere", []))
        
        # Architecture and village features
        architecture = random.choice(self.theme_config.get("architecture", []))
        village_feature = random.choice(self.theme_config.get("village_features", []))
        
        # Natural and magical elements
        natural_element = random.choice(self.theme_config.get("natural_elements", []))
        magical_element = random.choice(self.theme_config.get("magical_elements", []))
        
        # Time and weather
        time = random.choice(self.theme_config.get("time_of_day", []))
        weather = random.choice(self.theme_config.get("weather_effects", []))
        
        # Village life
        inhabitants = random.choice(self.theme_config.get("inhabitants", []))
        activity = random.choice(self.theme_config.get("activities", []))

        # Build the prompt
        prompt_parts = []
        
        # Add style and atmosphere
        prompt_parts.extend([style, atmosphere])
        
        # Add subject if provided
        if subject:
            prompt_parts.append(f"{subject} in a magical village setting")
        
        # Add location and architectural details
        if location:
            prompt_parts.append(f"in {location}")
        else:
            prompt_parts.extend([
                f"featuring {architecture}",
                f"with a {village_feature}"
            ])
        
        # Add natural and magical elements
        prompt_parts.extend([
            f"surrounded by {natural_element}",
            f"decorated with {magical_element}"
        ])
        
        # Add time and weather
        prompt_parts.extend([
            f"during {time}",
            f"with {weather}"
        ])
        
        # Add life and activity
        prompt_parts.extend([
            f"populated by {inhabitants}",
            f"during {activity}"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "modern buildings, urban setting, industrial elements, contemporary architecture, pollution, traffic, neon lights, modern technology, concrete jungle, dystopian elements"
