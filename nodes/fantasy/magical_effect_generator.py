from ...utils.common import handle_seed, flatten_dict_values
import random

class IsulionMagicalEffectGenerator:
    effects = {
        "fire": [
            "blazing aura", "flame burst", "phoenix wings", "inferno vortex",
            "fire storm", "molten rain", "ember dance", "solar flare",
            "dragon breath", "magma burst", "flame spiral", "burning sigil"
        ],
        "ice": [
            "frost crystals", "blizzard swirl", "arctic mist", "frozen aura",
            "glacial shield", "snow storm", "crystal frost", "ice spikes",
            "frozen time", "winter's embrace", "diamond dust", "absolute zero"
        ],
        "lightning": [
            "crackling energy", "thunder bolts", "static field", "plasma arc",
            "storm call", "chain lightning", "electric pulse", "voltage surge",
            "thunder strike", "spark shower", "static burst", "lightning storm"
        ],
        "nature": [
            "vine growth", "flower bloom", "leaf storm", "forest spirits",
            "thorny embrace", "pollen cloud", "root surge", "bark armor",
            "mushroom circle", "nature's wrath", "seed burst", "forest's blessing"
        ],
        "arcane": [
            "magical runes", "mystic circles", "astral projection", "ethereal wisps",
            "void portal", "time ripple", "reality bend", "mana surge",
            "spell matrix", "arcane symbols", "energy weave", "dimensional rift"
        ]
    }

    @classmethod
    def INPUT_TYPES(s):
        all_effects = flatten_dict_values(s.effects)
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
            seed = handle_seed(seed)
            
            if element != "any" and element in self.effects:
                effect = random.choice(self.effects[element])
            else:
                all_effects = flatten_dict_values(self.effects)
                effect = random.choice(all_effects)
        
        return (effect, seed) 