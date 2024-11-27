from .base_handler import BaseThemeHandler
from typing import Dict

class StreetFoodKebabThemeHandler(BaseThemeHandler):
    """Handler for generating street food kebab-themed prompts. Updated to reflect a blend of professional food photography and stylized illustration."""

    def generate_subject(self, custom_subject: str = "") -> str:
        if custom_subject:
            return custom_subject
            
        subjects = [
            "a gyro-style sub sandwich with a side of french fries",
            "an appetizing sub sandwich served with crispy fries",
            "a freshly prepared pita wrap accompanied by fries",
            "a vibrant wrap sandwich with golden fries",
            "a delicious sub with assorted fillings and fries"
        ]
        
        details = [
            "filled with various meats and vegetables",
            "accompanied by a side of golden brown fries",
            "wrapped in warm pita bread with fresh herbs",
            "served with a hint of creamy garlic sauce",
            "garnished with crisp lettuce and tomatoes"
        ]
        
        return f"{self.config.random.choice(subjects)}, {self.config.random.choice(details)}"

    def generate_environment(self, custom_location: str = "") -> str:
        if custom_location:
            return custom_location
            
        environments = [
            "in a restaurant or food service environment",
            "at a vibrant fast food stall",
            "in a cozy eatery with a side of fries",
            "on a bustling street corner with fries on the table",
            "in a high-end culinary setting with fries as a side"
        ]
        
        details = [
            "with a light brown wooden cutting board",
            "with a dark gray background",
            "surrounded by aromatic spices",
            "with dramatic lighting from the right",
            "on a dark surface, adding depth"
        ]
        
        return f"{self.config.random.choice(environments)}, {self.config.random.choice(details)}"

    def generate_style(self) -> str:
        styles = [
            "realistic and representational",
            "cartoonish and simplified",
            "high-end culinary photography",
            "stylized fast food illustration",
            "professional food photography"
        ]
        
        details = [
            "with a warm and appetizing color palette",
            "with exaggerated features for appeal",
            "with a focus on appetizing presentation",
            "emphasizing freshness and quality",
            "with vibrant colors against a dark background"
        ]
        
        return f"{self.config.random.choice(styles)}, {self.config.random.choice(details)}"

    def generate_effects(self) -> str:
        effects = [
            "controlled lighting from the right",
            "dramatic shadows enhancing depth",
            "vibrant color grading",
            "soft natural lighting",
            "crisp focus on the food"
        ]
        
        return self.config.random.choice(effects)

    def generate(self, custom_subject: str = "", 
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate street food kebab-themed components.
        
        Args:
            custom_subject (str): Custom subject override
            custom_location (str): Custom location override
            include_environment (str): Whether to include environment
            include_style (str): Whether to include style
            include_effects (str): Whether to include effects
            
        Returns:
            Dict[str, str]: Dictionary containing generated components
        """
        result = {
            "subject": self.generate_subject(custom_subject),
        }
        
        if include_environment.lower() == "yes":
            result["environment"] = self.generate_environment(custom_location)
            
        if include_style.lower() == "yes":
            result["style"] = self.generate_style()
            
        if include_effects.lower() == "yes":
            result["effects"] = self.generate_effects()
            
        return result