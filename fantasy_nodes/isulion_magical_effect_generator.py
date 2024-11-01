import random

class IsulionMagicalEffectGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "element": ("STRING", {"default": "any"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, seed=0, element="any"):
        random.seed(seed)
        effects = {
            "fire": ["blazing aura", "flame burst", "phoenix wings", "inferno vortex"],
            "ice": ["frost crystals", "blizzard swirl", "arctic mist", "frozen aura"],
            "lightning": ["crackling energy", "thunder bolts", "static field", "plasma arc"],
            "nature": ["vine growth", "flower bloom", "leaf storm", "forest spirits"],
            "arcane": ["magical runes", "mystic circles", "astral projection", "ethereal wisps"]
        }
        
        if element != "any" and element in effects:
            return (random.choice(effects[element]),)
        
        all_effects = [effect for sublist in effects.values() for effect in sublist]
        return (random.choice(all_effects),) 