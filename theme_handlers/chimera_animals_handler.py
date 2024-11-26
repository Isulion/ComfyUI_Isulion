from typing import Dict
from .base_handler import BaseThemeHandler

class ChimeraAnimalsThemeHandler(BaseThemeHandler):
    """Handler for chimera animals-themed prompt generation."""
    
    def _get_animal_family(self, animal: str) -> str:
        """Get the family classification of an animal."""
        try:
            animal_lower = animal.lower()
            for family in self.config_manager.get_config("animal_families"):
                if any(member.lower() in animal_lower for member in self.config_manager.get_config(f"animal_families.{family}")):
                    return family
            return None
        except Exception as e:
            print(f"Warning: Error getting animal family for {animal}: {str(e)}")
            return None

    def _get_safe_random_choice(self, config_key: str, default: str) -> str:
        """Safely get a random choice with fallback."""
        try:
            return self._get_random_choice(config_key)
        except Exception as e:
            print(f"Warning: Error getting choice for {config_key}: {str(e)}")
            return default

    def _get_safe_random_choices(self, config_key: str, count: int, defaults: list) -> list:
        """Safely get multiple random choices with fallback."""
        try:
            return self._get_random_choices(config_key, count)
        except Exception as e:
            print(f"Warning: Error getting choices for {config_key}: {str(e)}")
            return defaults[:count]

    def generate(self, custom_subject: str = "",
                custom_location: str = "",
                include_environment: str = "yes",
                include_style: str = "yes",
                include_effects: str = "yes") -> Dict[str, str]:
        """Generate chimera animals-themed components."""
        components = {}
        
        # Initialize variables
        max_attempts = 20
        head = None
        body = None
        
        if custom_subject:
            head = custom_subject
            head_family = self._get_animal_family(head)
            
            # Find complementary body animal
            while max_attempts > 0:
                body_candidate = self._get_safe_random_choice("animals", "Lion")
                body_family = self._get_animal_family(body_candidate)
                
                if (body_family != head_family and 
                    body_family is not None and 
                    head_family is not None and 
                    body_candidate.lower() != head.lower()):
                    body = body_candidate
                    break
                    
                max_attempts -= 1
        else:
            # Random selection of both animals
            while max_attempts > 0:
                head_candidate = self._get_safe_random_choice("animals", "Lion")
                body_candidate = self._get_safe_random_choice("animals", "Eagle")
                
                head_family = self._get_animal_family(head_candidate)
                body_family = self._get_animal_family(body_candidate)
                
                if (head_family != body_family and 
                    head_family is not None and 
                    body_family is not None and 
                    head_candidate.lower() != body_candidate.lower()):
                    head = head_candidate
                    body = body_candidate
                    break
                    
                max_attempts -= 1
        
        # Fallback to ensure valid animals
        if head is None or body is None:
            head = "Lion"  # From felines family
            body = "Eagle"  # From birds family
        
        # Create detailed subject description
        components["subject"] = (
            f"a complex raw photograph of an intricated chimerical fantastical creature with "
            f"((the body of a {body})) and ((the head of a {head})), "
            f"bokeh background, cinematic lighting, shallow depth of field, "
            f"35mm wide angle lens, sharp focus, cinematic film still, "
            f"dynamic angle, Photography, 8k, masterfully detailed, hyper-realistic"
        )
        
        # Generate environment if requested
        if include_environment == "yes":
            if custom_location:
                components["environment"] = (
                    f"in ((dramatic {custom_location})), "
                    f"((natural environment)), ((atmospheric depth)), "
                    f"((perfect composition))"
                )
            else:
                habitat = self._get_safe_random_choice("habitats", "mystical forest")
                weather = self._get_safe_random_choice("weather", "sunny")
                time = self._get_safe_random_choice("times", "day")
                components["environment"] = (
                    f"in a ((dramatic {habitat})) during {weather} {time}, "
                    f"((natural environment)), ((atmospheric depth)), "
                    f"((perfect composition))"
                )
        
        # Generate style if requested
        if include_style == "yes":
            components["style"] = (
                f"((professional wildlife photography)), ((ultra sharp focus)), "
                f"((perfect exposure)), ((dramatic composition)), "
                f"((photorealistic quality)), ((natural detail)), "
                f"8k resolution"
            )
        
        # Generate effects if requested
        if include_effects == "yes":
            components["effects"] = (
                f"with ((natural lighting)), ((atmospheric depth)), "
                f"((perfect shadows)), ((volumetric lighting)), "
                f"((cinematic atmosphere)), ((photographic realism))"
            )
        
        return components
