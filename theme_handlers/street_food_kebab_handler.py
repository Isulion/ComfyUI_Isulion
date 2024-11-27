from .base_handler import BaseThemeHandler
from typing import Dict

class StreetFoodKebabThemeHandler(BaseThemeHandler):
    """Handler for generating street food kebab-themed prompts."""

    def generate_subject(self, custom_subject: str = "") -> str:
        if custom_subject:
            return custom_subject
            
        subjects = [
            "a mouth-watering kebab sandwich",
            "an authentic döner kebab sandwich",
            "a freshly prepared shawarma sandwich",
            "a juicy kebab sandwich with thinly sliced meat",
            "a loaded kebab sandwich with grilled meat"
        ]
        
        details = [
            "stuffed with tender, marinated meat slices",
            "with crispy lettuce, fresh tomatoes, and red onions",
            "drizzled with creamy garlic sauce and spicy chili sauce",
            "wrapped in warm, fluffy pita bread",
            "garnished with fresh herbs and pickled vegetables",
            "with perfectly seasoned meat slices from the vertical rotisserie"
        ]
        
        return f"{self.config.random.choice(subjects)}, {self.config.random.choice(details)}"

    def generate_environment(self, custom_location: str = "") -> str:
        if custom_location:
            return custom_location
            
        environments = [
            "in a busy street food stall",
            "at a vibrant food market",
            "in a cozy kebab shop",
            "at a bustling street corner restaurant",
            "in an authentic Mediterranean eatery"
        ]
        
        details = [
            "with a rotating vertical meat spit in the background",
            "with steam rising from the grill",
            "surrounded by aromatic spices and fresh ingredients",
            "with warm lighting and rustic wooden surfaces",
            "next to traditional cooking equipment"
        ]
        
        return f"{self.config.random.choice(environments)}, {self.config.random.choice(details)}"

    def generate_style(self) -> str:
        styles = [
            "food photography style",
            "commercial food photography",
            "appetizing food styling",
            "natural lighting",
            "professional food magazine style",
            "high-end culinary photography"
        ]
        
        details = [
            "with rich colors and textures",
            "with mouth-watering details",
            "with perfect composition",
            "with shallow depth of field",
            "emphasizing freshness and quality"
        ]
        
        return f"{self.config.random.choice(styles)}, {self.config.random.choice(details)}"

    def generate_effects(self) -> str:
        effects = [
            "soft natural lighting",
            "subtle steam effects",
            "gentle bokeh background",
            "warm color grading",
            "slight vignetting",
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