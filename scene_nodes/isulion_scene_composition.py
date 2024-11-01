import random

class IsulionSceneComposition:
    compositions = {
        "angle": [
            "close-up shot", "wide angle", "birds eye view", "low angle",
            "dutch angle", "overhead shot", "eye-level shot", "high angle",
            "worms eye view", "tilted angle", "diagonal shot", "straight-on shot",
            "over-the-shoulder", "profile shot", "three-quarter view"
        ],
        "framing": [
            "panoramic view", "portrait shot", "landscape shot", "full body shot",
            "medium shot", "extreme close-up", "establishing shot", "tracking shot",
            "dolly shot", "zoom shot", "crane shot", "steadicam shot",
            "handheld shot", "static shot", "follow shot"
        ],
        "style": [
            "action shot", "dramatic angle", "symmetrical composition",
            "rule of thirds", "centered composition", "leading lines",
            "frame within frame", "silhouette", "minimalist composition",
            "dynamic composition", "geometric composition", "abstract composition",
            "balanced composition", "asymmetrical composition", "layered composition"
        ]
    }

    @classmethod
    def INPUT_TYPES(s):
        all_compositions = [comp for sublist in s.compositions.values() for comp in sublist]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "composition": (all_compositions,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "style": (["any", "angle", "framing", "style"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("composition", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Scene"

    def generate(self, randomize, composition, seed=0, style="any"):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            if style != "any" and style in self.compositions:
                composition = random.choice(self.compositions[style])
            else:
                all_compositions = [comp for sublist in self.compositions.values() for comp in sublist]
                composition = random.choice(all_compositions)
        
        return (composition, seed) 