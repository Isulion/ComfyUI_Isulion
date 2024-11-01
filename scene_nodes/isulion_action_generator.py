import random

class IsulionActionGenerator:
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
        actions = [
            "running", "jumping", "fighting", "casting spell", "dancing",
            "flying", "swimming", "climbing", "meditating", "reading",
            "wielding weapon", "performing ritual", "crafting"
        ]
        return (random.choice(actions),) 