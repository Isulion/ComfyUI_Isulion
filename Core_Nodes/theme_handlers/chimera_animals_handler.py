from typing import Dict
from .base_handler import BaseThemeHandler
import random

class ChimeraAnimalsThemeHandler(BaseThemeHandler):
    def _get_random_animal_from_category(self, category: str) -> str:
        """Get a random animal from a specific category."""
        animals = self.config.get_config(f"chimera_animals.categories.{category}")
        return random.choice(animals) if animals else "lion"

    def _get_different_category(self, exclude_category: str) -> str:
        """Get a random category different from the given one."""
        categories = list(self.config.get_config("chimera_animals.categories").keys())
        available_categories = [cat for cat in categories if cat != exclude_category]
        return random.choice(available_categories) if available_categories else "big_cats"

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate chimera animals-themed components."""
        components = {}
        
        # Initialize variables for head and body selection
        head = None
        body = None

        if custom_subject:
            # Use custom subject as the head
            head = custom_subject
            # For custom subjects, randomly select a category for the body
            # that's different from mythical
            body_category = self._get_different_category("mythical")
            body = self._get_random_animal_from_category(body_category)
        else:
            # Select two different random categories
            all_categories = list(self.config.get_config("chimera_animals.categories").keys())
            if not all_categories:
                # Fallback if categories are not found
                head = "lion"
                body = "eagle"
            else:
                head_category = random.choice(all_categories)
                body_category = self._get_different_category(head_category)
                
                # Get random animals from each category
                head = self._get_random_animal_from_category(head_category)
                body = self._get_random_animal_from_category(body_category)

        # Create the chimera description
        components["subject"] = (
            f"a majestic and powerful chimera creature with "
            f"((the head of a {head})) and ((the body of a {body})), "
            f"((detailed creature anatomy)), ((realistic animal features)), "
            f"((natural pose)), ((dynamic composition)), "
            f"((ultra-realistic)), ((masterful photography)), "
            f"((perfect lighting)), 8k resolution"
        )

        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in ((a majestic {custom_location})), "
                    f"((natural habitat)), ((atmospheric environment)), "
                    f"((perfect composition))"
                )
            else:
                environment_elements = [
                    self._get_safe_random_choice("chimera_animals.habitats", "mystical forest"),
                    self._get_safe_random_choice("chimera_animals.time_of_day", "golden hour"),
                    self._get_safe_random_choice("chimera_animals.weather", "clear sky")
                ]
                components["environment"] = (
                    f"in ((a majestic {environment_elements[0]})) during "
                    f"(({environment_elements[1]})) with (({environment_elements[2]})), "
                    f"((natural habitat)), ((atmospheric environment)), "
                    f"((perfect composition))"
                )

        # Generate style if requested
        if include_style:
            components["style"] = (
                f"((wildlife photography)), ((ultra-detailed)), "
                f"((perfect exposure)), ((dramatic composition)), "
                f"((photorealistic quality)), ((natural detail)), "
                f"((masterful technique))"
            )

        # Generate effects if requested
        if include_effects:
            components["effects"] = (
                f"with ((natural lighting)), ((volumetric atmosphere)), "
                f"((perfect shadows)), ((depth of field)), "
                f"((cinematic mood)), ((photographic excellence))"
            )

        return components
