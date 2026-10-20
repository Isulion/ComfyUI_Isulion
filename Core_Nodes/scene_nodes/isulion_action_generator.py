from ..base_selector import SimpleSelectorNode


class IsulionActionGenerator(SimpleSelectorNode):
    POOL = [
        "running", "jumping", "fighting", "casting spell", "dancing",
        "flying", "swimming", "climbing", "meditating", "reading",
        "wielding weapon", "performing ritual", "crafting"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "action": (s.POOL,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("action", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Scene"

    def generate(self, randomize, action, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            action = rng.choice(self._pool_for())

        return (action, seed)
