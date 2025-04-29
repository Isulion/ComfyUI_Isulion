from typing import Dict
from .base_handler import BaseThemeHandler

class StarWarsThemeHandler(BaseThemeHandler):
    """Handler for Star Wars universe-themed prompt generation with cinematic quality and authentic details."""
    
    def __init__(self, config):
        super().__init__(config)
        self.theme_config = config.get_config("star_wars")
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate sophisticated Star Wars universe-themed components with cinematic quality."""
        components = {}

        # Always use random elements, even with custom_subject
        pose = self._get_random_choice("star_wars.poses")
        prop = self._get_random_choice("star_wars.props")
        character = self._get_random_choice("star_wars.characters")

        # Generate subject with enhanced Star Wars elements
        if custom_subject:
            components["subject"] = (
                f"((epic Star Wars universe scene)) of ((masterfully crafted {custom_subject})), "
                f"((wielding glowing {prop})), ((in {pose})), "
                f"((perfect Star Wars design)), ((authentic sci-fi details)), "
                f"((cinematic quality)), ((epic scale)), ((dramatic pose)), "
                f"((photorealistic detail)), ((Star Wars excellence)), "
                f"((movie quality)), ((ILM VFX style))"
            )
        else:
            scene_type = self._get_random_choice("star_wars.scene_types")
            if scene_type == "character":
                character = self._get_random_choice("star_wars.characters")
                prop = self._get_random_choice("star_wars.props")
                pose = self._get_random_choice("star_wars.poses")
                components["subject"] = (
                    f"((epic Star Wars cinematic scene)) of ((highly detailed {character})) "
                    f"((wielding glowing {prop})), ((in {pose})), "
                    f"((perfect Star Wars design)), ((authentic character details)), "
                    f"((dramatic pose)), ((epic scale)), ((photorealistic quality)), "
                    f"((Star Wars universe)), ((movie excellence))"
                )
            elif scene_type == "vehicle":
                vehicle = self._get_random_choice("star_wars.vehicles")
                character = self._get_random_choice("star_wars.characters")
                action = self._get_random_choice("star_wars.actions")
                components["subject"] = (
                    f"((dramatic Star Wars shot)) of ((highly detailed {vehicle})) "
                    f"with ((detailed {character})) ((performing {action})), "
                    f"((epic space battle scene)), ((perfect vehicle design)), "
                    f"((authentic Star Wars details)), ((cinematic quality)), "
                    f"((dramatic composition)), ((photorealistic rendering))"
                )
            else:  # battle scene
                character = self._get_random_choice("star_wars.characters")
                prop = self._get_random_choice("star_wars.props")
                vehicle = self._get_random_choice("star_wars.vehicles")
                battle = self._get_random_choice("star_wars.battles")
                components["subject"] = (
                    f"((epic Star Wars battle scene)) of ((masterfully crafted {battle})) "
                    f"with ((detailed {character})) using ((powerful {prop})) "
                    f"near ((massive {vehicle})), ((intense action)), "
                    f"((perfect battle choreography)), ((authentic Star Wars combat)), "
                    f"((cinematic excellence)), ((epic scale))"
                )

        # Generate environment with enhanced Star Wars atmosphere
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((masterfully crafted {custom_location})), "
                    f"((authentic Star Wars atmosphere)), ((epic sci-fi environment)), "
                    f"((massive scale)), ((otherworldly vista)), "
                    f"((perfect Star Wars architecture)), ((dramatic lighting)), "
                    f"((cinematic environment)), ((photorealistic details))"
                )
            else:
                location = self._get_random_choice("star_wars.locations")
                environment = self._get_random_choice("star_wars.environments")
                structure = self._get_random_choice("star_wars.structures")
                atmosphere = self._get_random_choice("star_wars.atmospheres")
                components["environment"] = (
                    f"in ((masterfully crafted {location})) with ((epic {environment})), "
                    f"((featuring massive {structure})), ((in {atmosphere} atmosphere)), "
                    f"((authentic Star Wars setting)), ((perfect sci-fi architecture)), "
                    f"((otherworldly vista)), ((dramatic lighting)), "
                    f"((cinematic environment)), ((photorealistic details))"
                )

        # Generate style with enhanced cinematic quality
        if include_style == "yes":
            style = self._get_random_choice("star_wars.styles")
            lighting = self._get_random_choice("star_wars.lighting")
            color = self._get_random_choice("star_wars.color_schemes")
            technique = self._get_random_choice("star_wars.techniques")
            components["style"] = (
                f"((masterful {style} style)), ((authentic Star Wars aesthetic)), "
                f"((featuring {lighting})), ((with {color} color scheme)), "
                f"((using {technique})), ((ILM VFX quality)), "
                f"((cinematic excellence)), ((photorealistic detail)), "
                f"((professional cinematography)), ((epic movie scene)), "
                f"((high production value)), ((perfect composition)), "
                f"((professional color grading)), 8k resolution"
            )

        # Generate effects with enhanced Star Wars elements
        if include_effects == "yes":
            effect = self._get_random_choice("star_wars.effects")
            element = self._get_random_choice("star_wars.elements")
            particle = self._get_random_choice("star_wars.particles")
            ambiance = self._get_random_choice("star_wars.ambiance")
            components["effects"] = (
                f"with ((masterful {effect})), ((authentic {element})), "
                f"((featuring {particle})), ((in {ambiance} ambiance)), "
                f"((Star Wars VFX)), ((cinematic effects)), "
                f"((dramatic lighting)), ((lens flares)), "
                f"((volumetric lighting)), ((perfect atmosphere)), "
                f"((photorealistic rendering)), ((movie quality))"
            )

        return components

    def get_negative_prompt(self):
        """Generate comprehensive negative prompt for Star Wars theme."""
        return (
            "((amateur sci-fi)), ((poor VFX)), ((bad lighting)), "
            "((inconsistent style)), ((wrong Star Wars elements)), "
            "((non-canon designs)), ((poor composition)), "
            "((stiff poses)), ((unrealistic effects)), "
            "((wrong perspective)), ((missing details)), "
            "((flat lighting)), ((amateur rendering)), "
            "((weak atmosphere)), ((incorrect Star Wars lore)), "
            "((poor cinematography)), ((low budget)), "
            "((incorrect scale)), ((missing drama)), "
            "((low quality)), ((blurry)), ((noisy)), ((pixelated)), "
            "((wrong sci-fi style)), ((incorrect universe)), "
            "((bad special effects)), ((poor character design)), "
            "((incorrect technology)), ((wrong architectural style))"
        )
