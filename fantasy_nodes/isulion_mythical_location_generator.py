import random

class IsulionMythicalLocationGenerator:
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
    CATEGORY = "Isulion/Fantasy"

    def generate(self, seed=0):
        random.seed(seed)
        locations = [
            "crystal cave", "floating islands", "ancient temple", "enchanted forest",
            "dragon's lair", "wizard's tower", "fairy grove", "rainbow bridge",
            "underwater palace", "cloud castle", "phoenix nest", "mystic library",
            "forgotten ruins", "elemental sanctuary", "starlit grove", "demon realm"
        ]
        return (random.choice(locations),) 