import random

class IsulionStyleMixer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "style1": ("STRING", {"forceInput": True}),
                "style2": ("STRING", {"forceInput": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "blend_mode": (["balanced", "style1_dominant", "style2_dominant"], {"default": "balanced"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "mix"
    CATEGORY = "Isulion/Enhancement"

    def mix(self, style1, style2, seed=0, blend_mode="balanced"):
        random.seed(seed)
        
        # Common connecting words for style mixing
        connectors = {
            "balanced": ["mixed with", "combined with", "blended with", "fused with"],
            "style1_dominant": ["with subtle elements of", "with hints of", "slightly influenced by"],
            "style2_dominant": ["incorporating", "heavily influenced by", "dominated by elements of"]
        }
        
        connector = random.choice(connectors[blend_mode])
        mixed_style = f"{style1} {connector} {style2}"
        
        return (mixed_style,) 