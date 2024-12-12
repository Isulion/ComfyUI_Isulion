import random

class IsulionMagicalEffectGenerator:
    effects = {
        "fire": ["blazing aura", "flame burst", "phoenix wings", "inferno vortex"],
        "ice": ["frost crystals", "blizzard swirl", "arctic mist", "frozen aura"],
        "lightning": ["crackling energy", "thunder bolts", "static field", "plasma arc"],
        "nature": ["vine growth", "flower bloom", "leaf storm", "forest spirits"],
        "arcane": ["magical runes", "mystic circles", "astral projection", "ethereal wisps"]
    }

    @classmethod
    def INPUT_TYPES(s):
        all_effects = [effect for sublist in s.effects.values() for effect in sublist]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "effect": (all_effects,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "element": (["any", "fire", "ice", "lightning", "nature", "arcane"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("effect", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, randomize, effect, seed=0, element="any"):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            if element != "any" and element in self.effects:
                effect = random.choice(self.effects[element])
            else:
                all_effects = [e for sublist in self.effects.values() for e in sublist]
                effect = random.choice(all_effects)
        
        return (effect, seed) 