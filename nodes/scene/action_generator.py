from ...utils.common import handle_seed
import random

class IsulionActionGenerator:
    actions = [
        # ... existing actions list ...
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "action": (s.actions,),
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
        if randomize == "enable":
            seed = handle_seed(seed)
            action = random.choice(self.actions)
        
        return (action, seed) 