from .base_handler import BaseThemeHandler
from typing import Dict

class StreetFoodKebabThemeHandler(BaseThemeHandler):
    """Handler for generating street food kebab-themed prompts. Updated to reflect a blend of professional food photography and stylized illustration."""

    def generate_subject(self, custom_subject: str = "") -> str:
        if custom_subject:
            return custom_subject
            
        subjects = [
            "a classic French-style kebab with golden frites",
            "a loaded kebab sandwich overflowing with meat and crispy fries",
            "an authentic Parisian street kebab with herb-seasoned frites",
            "a generous kebab platter topped with golden french fries",
            "a vibrant street-style kebab with perfectly crisp frites"
        ]
        
        details = [
            "drizzled with spicy harissa mayo",
            "garnished with caramelized onions",
            "served with a side of perfectly golden fries",
            "accompanied by a zesty herb sauce",
            "topped with fresh parsley and crisp vegetables"
        ]
        
        return f"{self.config.random.choice(subjects)}, {self.config.random.choice(details)}"

    def generate_environment(self, custom_location: str = "") -> str:
        if custom_location:
            return custom_location
            
        environments = [
            "on a bustling Parisian street corner",
            "at an authentic French street food cart",
            "in a vibrant urban kebab stand",
            "along a traditional Paris street food setting",
            "within a lively urban food market"
        ]
        
        details = [
            "with warm ambient street lighting",
            "featuring a rotating meat spit in the background",
            "surrounded by the energy of urban street cuisine",
            "with a glimpse of the city's culinary culture",
            "capturing the essence of street food preparation"
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