import random

class IsulionAlienWorldGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, seed=0):
        random.seed(seed)
        
        atmospheres = ["toxic", "breathable", "dense", "thin", "crystalline"]
        terrains = ["crystalline desert", "floating islands", "metallic plains", "bio-luminescent jungle", 
                   "liquid methane ocean", "plasma storms", "geometric mountains", "silicon forests"]
        colors = ["purple", "emerald", "crimson", "azure", "golden"]
        features = ["multiple moons", "binary suns", "ring system", "quantum anomalies", "temporal rifts"]
        
        world_desc = f"{random.choice(colors)} world with {random.choice(atmospheres)} atmosphere, " \
                    f"featuring {random.choice(terrains)} and {random.choice(features)}"
        
        return (world_desc,) 