from .base_handler import BaseThemeHandler
from typing import Dict

class StreetFoodKebabThemeHandler(BaseThemeHandler):
    """Handler for generating street food kebab-themed prompts. Updated to reflect a blend of professional food photography and stylized illustration."""

    def generate_subject(self, custom_subject: str = "") -> str:
        if custom_subject:
            return custom_subject
            
        breads = [
            "pita bread",
            "large crusty bread roll",
            "toasted flatbread",
            "soft white bread",
            "warm pita wrap"
        ]
        
        meats = [
            "grilled chicken pieces",
            "sliced pieces of grilled meat",
            "shredded chicken",
            "tender grilled lamb",
            "seasoned shredded beef"
        ]
        
        vegetables = [
            "fresh lettuce, cucumber, tomato, and red onion",
            "crisp lettuce, juicy tomato slices, and red onions",
            "mixed fresh vegetables",
            "crunchy lettuce and sliced tomatoes",
            "garden-fresh vegetable mix"
        ]
        
        sauces = [
            "creamy white sauce",
            "tangy tzatziki",
            "garlic aioli",
            "spicy herb sauce",
            "creamy ranch dressing"
        ]
        
        fries_descriptions = [
            "golden and crispy French fries",
            "freshly cooked crisp fries",
            "perfectly golden French fries",
            "hot, crispy potato fries",
            "golden-brown crispy fries"
        ]
        
        subject_template = "a close-up of a delicious-looking kebab sandwich served with {fries}. The sandwich is made with {bread} filled with {meat}, {vegetables}. The sandwich is topped with {sauce}. The French fries are {fries_desc}, placed next to the sandwich."
        
        return subject_template.format(
            bread=self.config.random.choice(breads),
            meat=self.config.random.choice(meats),
            vegetables=self.config.random.choice(vegetables),
            sauce=self.config.random.choice(sauces),
            fries=self.config.random.choice(fries_descriptions),
            fries_desc=self.config.random.choice(fries_descriptions)
        )

    def generate_environment(self, custom_location: str = "") -> str:
        if custom_location:
            return custom_location
            
        backgrounds = [
            "dark background which makes the food stand out prominently",
            "black plate highlighting the food's colors",
            "matte black surface creating contrast",
            "deep charcoal background",
            "shadowy background emphasizing the food"
        ]
        
        lighting = [
            "soft side lighting",
            "dramatic overhead light",
            "warm, focused lighting",
            "studio-style food photography lighting",
            "carefully controlled directional light"
        ]
        
        placement = [
            "neatly arranged on a clean surface",
            "positioned to showcase both the sandwich and fries",
            "carefully composed food styling",
            "artfully displayed with attention to detail",
            "strategically placed for maximum visual appeal"
        ]
        
        return f"on {self.config.random.choice(backgrounds)}, with {self.config.random.choice(lighting)}, {self.config.random.choice(placement)}"

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