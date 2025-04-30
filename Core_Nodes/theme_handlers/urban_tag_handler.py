from typing import Dict
from .base_handler import BaseThemeHandler

class UrbanTagThemeHandler(BaseThemeHandler):
    """Handler for urban tag and street art-themed prompt generation."""
    
    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: bool = True,
                include_style: bool = True,
                include_effects: bool = True) -> Dict[str, str]:
        """Generate urban tag and street art-themed components."""
        components = {}
        
        # Get base elements
        style = self._get_random_choice("urban_tag.styles")
        effect = self._get_random_choice("urban_tag.effects")
        color_scheme = self._get_random_choice("urban_tag.colors")
        base_desc = self._get_random_choice("urban_tag.base_descriptions")
        
        # Generate subject
        if custom_subject:
            components["subject"] = (
                f"(({base_desc})) of {custom_subject}, "
                f"((with various details spray-painted)), "
                f"((urban art interpretation)), ((street art character)), "
                f"((in {style})), ((street art aesthetic)), "
                f"((urban culture)), ((graffiti art style)), "
                f"((with {color_scheme} color scheme)), "
                f"((stylized urban character)), ((not realistic)), "
                f"((street art portrait))"
            )
        else:
            text = self._get_random_choice("urban_tag.text_options")
            components["subject"] = (
                f"(({base_desc})) of {text}, "
                f"((with various details spray-painted)), "
                f"((in {style})), ((street art aesthetic)), "
                f"((graffiti lettering)), ((urban culture)), "
                f"((with {color_scheme} color scheme)), "
                f"((dynamic typography))"
            )
        
        # Generate environment if requested
        if include_environment:
            if custom_location:
                components["environment"] = (
                    f"in (({custom_location})), ((with urban texture)), "
                    f"((city atmosphere)), ((street culture)), "
                    f"((urban decay)), ((metropolitan setting))"
                )
            else:
                surface = self._get_random_choice("urban_tag.surfaces")
                location = self._get_random_choice("urban_tag.locations")
                components["environment"] = (
                    f"on ((urban {surface})) in (({location})), "
                    f"((with urban texture)), ((city atmosphere)), "
                    f"((street culture)), ((urban decay)), "
                    f"((metropolitan setting))"
                )
        
        # Generate style if requested
        if include_style:
            atmosphere = self._get_random_choice("urban_tag.atmospheres")
            components["style"] = (
                f"((street art style)), ((graffiti aesthetic)), "
                f"((urban art)), ((spray paint technique)), "
                f"((professional street art)), ((urban culture)), "
                f"((stylized urban art)), ((graffiti character design)), "
                f"((street art interpretation)), ((not photorealistic)), "
                f"((complex fresco style)), ((hip hop culture)), "
                f"8k resolution"
            )
        
        # Generate effects if requested
        if include_effects:
            effect = self._get_random_choice("urban_tag.effects")
            components["effects"] = (
                f"with (({effect})), ((urban textures)), "
                f"((street art finish)), ((graffiti effects)), "
                f"((spray paint details)), ((metropolitan atmosphere)), "
                f"((stylized urban artwork)), ((street art character)), "
                f"((multicolored spray paint)), ((detailed fresco))"
            )
        
        return components
