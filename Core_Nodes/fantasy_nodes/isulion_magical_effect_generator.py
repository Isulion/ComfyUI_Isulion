from ..base_selector import SimpleSelectorNode


class IsulionMagicalEffectGenerator(SimpleSelectorNode):
    POOLS = {
        "fire": ["blazing aura", "flame burst", "phoenix wings", "inferno vortex"],
        "ice": ["frost crystals", "blizzard swirl", "arctic mist", "frozen aura"],
        "lightning": ["crackling energy", "thunder bolts", "static field", "plasma arc"],
        "nature": ["vine growth", "flower bloom", "leaf storm", "forest spirits"],
        "arcane": ["magical runes", "mystic circles", "astral projection", "ethereal wisps"]
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "effect": (s._pool_for(),),
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
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            effect = rng.choice(self._pool_for(element))

        return (effect, seed)
