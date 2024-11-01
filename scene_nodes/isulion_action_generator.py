import random

class IsulionActionGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "action": (["running", "jumping", "fighting", "casting spell", "dancing",
                          "flying", "swimming", "climbing", "meditating", "reading",
                          "wielding weapon", "performing ritual", "crafting"],),
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
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            action = random.choice(self.INPUT_TYPES()["required"]["action"][0])
        
        return (action, seed) 