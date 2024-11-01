from ...utils.common import handle_seed
import random

class IsulionStyleMixer:
    # ... existing connectors dictionary ...

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "style1": ("STRING", {"default": ""}),
                "style2": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "blend_mode": (["balanced", "style1_dominant", "style2_dominant"], {"default": "balanced"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("mixed_style", "seed",)
    FUNCTION = "mix"
    CATEGORY = "Isulion/Enhancement"

    def mix(self, randomize, style1, style2, seed=0, blend_mode="balanced"):
        if randomize == "enable":
            seed = handle_seed(seed)
            connector = random.choice(self.connectors[blend_mode])
        else:
            connector = self.connectors[blend_mode][0]
            
        mixed_style = f"{style1} {connector} {style2}"
        return (mixed_style, seed) 