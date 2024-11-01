import random

class IsulionPromptGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("prompt", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Core"

    def generate(self, prompt, seed=0):
        if seed is not None and seed > 0:
            random.seed(seed)
        else:
            seed = random.randint(0, 0xffffffffffffffff)
            random.seed(seed)
        
        return (prompt, seed) 