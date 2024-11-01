import random

class IsulionArtifactGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "type": ("STRING", {"default": "any"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, seed=0, type="any"):
        random.seed(seed)
        artifacts = {
            "weapon": ["legendary sword", "mystic staff", "enchanted bow", "divine spear"],
            "jewelry": ["power amulet", "magic ring", "crystal crown", "soul gem"],
            "tool": ["seeing glass", "teleport stone", "wisdom scroll", "healing chalice"],
            "relic": ["ancient tablet", "dragon scale", "phoenix feather", "unicorn horn"]
        }
        
        if type != "any" and type in artifacts:
            return (random.choice(artifacts[type]),)
            
        all_artifacts = [item for sublist in artifacts.values() for item in sublist]
        return (random.choice(all_artifacts),) 