from ...utils.common import handle_seed, flatten_dict_values
import random

class IsulionTechGenerator:
    technology = {
        # ... existing technology dictionary ...
    }

    @classmethod
    def INPUT_TYPES(s):
        all_tech = flatten_dict_values(s.technology)
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "tech": (all_tech,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "tech_type": (["any", "weapons", "gadgets", "augments", "power"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("tech", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, randomize, tech, seed=0, tech_type="any"):
        if randomize == "enable":
            seed = handle_seed(seed)
            
            if tech_type != "any" and tech_type in self.technology:
                tech = random.choice(self.technology[tech_type])
            else:
                all_tech = flatten_dict_values(self.technology)
                tech = random.choice(all_tech)
        
        return (tech, seed) 