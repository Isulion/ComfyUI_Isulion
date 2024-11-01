import random

class IsulionStyleMixer:
    connectors = {
        "balanced": [
            "mixed with", "combined with", "blended with", "fused with",
            "merged with", "unified with", "integrated with", "harmonized with",
            "synthesized with", "joined with", "intertwined with", "woven with"
        ],
        "style1_dominant": [
            "with subtle elements of", "with hints of", "slightly influenced by",
            "with touches of", "mildly incorporating", "with nuances of",
            "with undertones of", "with accents of", "lightly seasoned with",
            "with gentle notes of", "with delicate traces of", "softly embracing"
        ],
        "style2_dominant": [
            "incorporating", "heavily influenced by", "dominated by elements of",
            "strongly featuring", "primarily driven by", "deeply infused with",
            "substantially merged with", "predominantly showing", "mainly characterized by",
            "significantly shaped by", "largely defined by", "powerfully combined with"
        ]
    }

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
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            connector = random.choice(self.connectors[blend_mode])
        else:
            connector = self.connectors[blend_mode][0]
            
        mixed_style = f"{style1} {connector} {style2}"
        return (mixed_style, seed) 