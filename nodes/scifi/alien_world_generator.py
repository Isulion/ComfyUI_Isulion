from ...utils.common import handle_seed
import random

class IsulionAlienWorldGenerator:
    atmospheres = [
        # ... existing atmospheres list ...
    ]
    
    terrains = [
        # ... existing terrains list ...
    ]
    
    colors = [
        # ... existing colors list ...
    ]
    
    features = [
        # ... existing features list ...
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "atmosphere": (s.atmospheres,),
                "terrain": (s.terrains,),
                "color": (s.colors,),
                "feature": (s.features,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("world_desc", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, randomize, atmosphere, terrain, color, feature, seed=0):
        if randomize == "enable":
            seed = handle_seed(seed)
            
            atmosphere = random.choice(self.atmospheres)
            terrain = random.choice(self.terrains)
            color = random.choice(self.colors)
            feature = random.choice(self.features)
        
        world_desc = f"{color} world with {atmosphere} atmosphere, featuring {terrain} and {feature}"
        return (world_desc, seed) 