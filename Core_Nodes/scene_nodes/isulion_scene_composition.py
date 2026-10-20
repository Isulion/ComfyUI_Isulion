from ..base_selector import SimpleSelectorNode


class IsulionSceneComposition(SimpleSelectorNode):
    POOL = [
        "close-up shot", "wide angle", "birds eye view", "low angle",
        "dutch angle", "panoramic view", "portrait shot", "action shot",
        "dramatic angle", "symmetrical composition"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "composition": (s.POOL,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("composition", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Scene"

    def generate(self, randomize, composition, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            composition = rng.choice(self._pool_for())

        return (composition, seed)
