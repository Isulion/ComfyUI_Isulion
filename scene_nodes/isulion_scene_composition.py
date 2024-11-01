import random

class IsulionSceneComposition:
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
    CATEGORY = "Isulion/Scene"

    def generate(self, seed=0):
        random.seed(seed)
        compositions = [
            "close-up shot", "wide angle", "birds eye view", "low angle",
            "dutch angle", "panoramic view", "portrait shot", "action shot",
            "dramatic angle", "symmetrical composition"
        ]
        return (random.choice(compositions),) 