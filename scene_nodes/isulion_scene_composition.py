import random

class IsulionSceneComposition:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "composition": (["close-up shot", "wide angle", "birds eye view", "low angle",
                               "dutch angle", "panoramic view", "portrait shot", "action shot",
                               "dramatic angle", "symmetrical composition"],),
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
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            composition = random.choice(self.INPUT_TYPES()["required"]["composition"][0])
        
        return (composition, seed) 