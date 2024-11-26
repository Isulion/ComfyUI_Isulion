from typing import Dict
from .base_handler import BaseThemeHandler

class CulinaryFoodThemeHandler(BaseThemeHandler):
    """Handler for culinary/food-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate culinary/food-themed components."""
        components = {}
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"((culinary {custom_subject})), "
                f"((food photography)), ((gourmet presentation)), "
                f"((professional food styling))"
            )
        else:
            dish = self._get_random_choice("culinary_food.dishes")
            cuisine = self._get_random_choice("culinary_food.cuisines")
            feature = self._get_random_choice("culinary_food.features")
            components["subject"] = (
                f"((culinary {dish} from {cuisine} cuisine)), "
                f"((featuring {feature})), ((food photography)), "
                f"((gourmet presentation)), ((professional food styling))"
            )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((culinary {custom_location})) with "
                    f"((food setting)), ((professional staging))"
                )
            else:
                setting = self._get_random_choice("culinary_food.settings")
                prop = self._get_random_choice("culinary_food.props")
                components["environment"] = (
                    f"in ((culinary {setting})) with "
                    f"((food {prop})), "
                    f"((professional staging)), ((culinary background)), "
                    f"((gourmet environment))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            style = self._get_random_choice("culinary_food.styles")
            technique = self._get_random_choice("culinary_food.techniques")
            components["style"] = (
                f"((styled in {style} manner)), "
                f"((using {technique} technique)), "
                f"((culinary artistry)), ((food styling)), "
                f"((professional presentation))"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            effect = self._get_random_choice("culinary_food.effects")
            lighting = self._get_random_choice("culinary_food.lighting")
            components["effects"] = (
                f"with ((culinary {effect} effects)), "
                f"((food {lighting} lighting)), "
                f"((gourmet quality)), ((professional finish))"
            )
        
        return components
