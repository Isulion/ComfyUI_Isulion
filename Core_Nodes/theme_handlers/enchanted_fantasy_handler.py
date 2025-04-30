import random
from typing import Dict
from .base_handler import BaseThemeHandler

class EnchantedFantasyThemeHandler(BaseThemeHandler):
    """Handler for enchanted fantasy-themed prompt generation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("enchanted_fantasy")

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate enchanted fantasy-themed components."""
        components = {}
        
        # Always use random elements, even with custom_subject
        feature = self._get_random_choice("enchanted_fantasy.features")
        realm = self._get_random_choice("enchanted_fantasy.realms")

        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((enchanted {custom_subject} from {realm})), "
                f"((featuring {feature})), ((magical being)), "
                f"((fantasy creature)), ((mystical character))"
            )
        else:
            being = self._get_random_choice("enchanted_fantasy.beings")
            realm = self._get_random_choice("enchanted_fantasy.realms")
            feature = self._get_random_choice("enchanted_fantasy.features")
            components["subject"] = (
                f"((enchanted {being} from {realm})), "
                f"((featuring {feature})), ((magical being)), "
                f"((fantasy creature)), ((mystical character))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((enchanted {custom_location})) with "
                    f"((magical setting)), ((fantasy realm))"
                )
            else:
                setting = self._get_random_choice("enchanted_fantasy.settings")
                element = self._get_random_choice("enchanted_fantasy.elements")
                components["environment"] = (
                    f"in ((enchanted {setting})) with "
                    f"((magical {element})), "
                    f"((fantasy environment)), ((mystical world)), "
                    f"((enchanted realm))"
                )
        
        # Generate style if requested
        if include_style:
            style = self._get_random_choice("enchanted_fantasy.styles")
            magic = self._get_random_choice("enchanted_fantasy.magic")
            components["style"] = (
                f"((styled with {style} magic)), "
                f"((using {magic} powers)), "
                f"((enchanted artistry)), ((fantasy aesthetic)), "
                f"((magical quality))"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("enchanted_fantasy.effects")
            aura = self._get_random_choice("enchanted_fantasy.auras")
            components["effects"] = (
                f"with ((magical {effect} effects)), "
                f"((enchanted {aura} aura)), "
                f"((mystical atmosphere)), ((fantasy ambiance))"
            )
        
        return components

    def generate_theme_prompt(self, subject=None, location=None):
        # Base style and atmosphere
        style = random.choice(self.theme_config.get("styles", []))
        atmosphere = random.choice(self.theme_config.get("atmosphere", []))
        
        # Magical elements and artifacts
        magical_element = random.choice(self.theme_config.get("magical_elements", []))
        artifact = random.choice(self.theme_config.get("artifacts", []))
        
        # Environment and architecture
        environment = random.choice(self.theme_config.get("environments", [])) if not location else location
        architecture = random.choice(self.theme_config.get("architectural_elements", []))
        
        # Lighting and atmosphere
        lighting = random.choice(self.theme_config.get("lighting_effects", []))
        time = random.choice(self.theme_config.get("time_of_day", []))
        weather = random.choice(self.theme_config.get("weather_effects", []))
        
        # Color and creatures
        color_scheme = random.choice(self.theme_config.get("color_schemes", []))
        creature = random.choice(self.theme_config.get("creatures", []))

        # Build the prompt
        prompt_parts = []
        
        # Add style and atmosphere
        prompt_parts.extend([style, atmosphere])
        
        # Add subject if provided
        if subject:
            prompt_parts.append(f"{subject} in an enchanted fantasy setting")
        
        # Add environment and architectural details
        if location:
            prompt_parts.append(f"in {location}")
        else:
            prompt_parts.extend([
                f"in a {environment}",
                f"with {architecture}"
            ])
        
        # Add magical elements and artifacts
        prompt_parts.extend([
            f"surrounded by {magical_element}",
            f"featuring {artifact}"
        ])
        
        # Add lighting and atmosphere
        prompt_parts.extend([
            lighting,
            f"during {time}",
            f"with {weather}"
        ])
        
        # Add color and creatures
        prompt_parts.extend([
            color_scheme,
            f"with {creature} in the scene"
        ])
        
        # Join all parts with commas
        prompt = ", ".join(prompt_parts)
        
        return prompt

    def get_negative_prompt(self):
        return "modern elements, urban setting, technology, sci-fi, contemporary, mundane, ordinary, realistic, gritty, dark horror, gore, disturbing elements"
