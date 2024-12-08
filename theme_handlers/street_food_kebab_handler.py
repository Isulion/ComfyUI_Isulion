from .base_handler import BaseThemeHandler
from typing import Dict

class StreetFoodKebabThemeHandler(BaseThemeHandler):
    """Handler for generating street food kebab-themed prompts. Updated to reflect a blend of professional food photography and stylized illustration."""

    def generate_subject(self, custom_subject: str = "") -> str:
        if custom_subject:
            return custom_subject
            
        breads = [
            "traditional Turkish bread wrap",
            "freshly baked döner bread",
            "crisp lavash bread",
            "soft pita bread",
            "warm Turkish flatbread"
        ]
        
        meats = [
            "thinly sliced seasoned lamb",
            "tender grilled chicken döner",
            "marinated beef döner",
            "mixed meat döner",
            "spiced lamb and chicken blend"
        ]
        
        vegetables = [
            "crisp lettuce, cucumber, tomato, and red cabbage",
            "fresh mixed salad with red onions",
            "crunchy lettuce, juicy tomatoes, and pickled vegetables",
            "garden-fresh cucumber, tomato, and red onion mix",
            "traditional Turkish vegetable medley"
        ]
        
        sauces = [
            "creamy garlic sauce",
            "traditional white döner sauce",
            "spicy red pepper sauce",
            "herb-infused yogurt sauce",
            "tangy Mediterranean sauce"
        ]
        
        fries_descriptions = [
            "golden and crispy Turkish-style fries",
            "freshly cooked crisp potato wedges",
            "perfectly golden Mediterranean fries",
            "hot, seasoned potato fries",
            "golden-brown crispy side fries"
        ]
        
        packaging_details = [
            "a traditional döner wrap paper",
            "an authentic Turkish street food packaging",
            "a branded döner kebab wrapper",
            "a rustic food service paper",
            "a classic döner presentation wrap"
        ]
        
        sauce_details = [
            "three small containers of sauces: white, red, and herb-green",
            "a variety of traditional döner sauces",
            "multiple authentic Turkish condiments",
            "artfully arranged sauce selection",
            "classic döner accompaniment sauces"
        ]
        
        subject_template = "an authentic image of a döner kebab featuring {bread} filled with {meat}, layered with {vegetables}, and topped with {sauce}. {packaging} is visible beside the kebab. {sauce_containers} complement the meal. The {fries_desc} are served alongside, creating a traditional Turkish street food scene."
        
        return subject_template.format(
            bread=self.config.random.choice(breads),
            meat=self.config.random.choice(meats),
            vegetables=self.config.random.choice(vegetables),
            sauce=self.config.random.choice(sauces),
            packaging=self.config.random.choice(packaging_details),
            sauce_containers=self.config.random.choice(sauce_details),
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