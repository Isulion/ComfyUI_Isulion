import random

class IsulionNegativePromptGenerator:
    negative_elements = {
        "basic": [
            "blurry", "pixelated", "low quality", "watermark",
            "signature", "text", "bad anatomy", "distorted",
            "poor quality", "low resolution", "jpeg artifacts",
            "compression artifacts", "poorly drawn", "bad proportions"
        ],
        "standard": [
            "deformed", "disfigured", "poorly drawn", "extra limbs",
            "cloned face", "gross proportions", "malformed limbs",
            "missing arms", "missing legs", "extra arms", "extra legs",
            "fused fingers", "too many fingers", "long neck",
            "mutation", "mutated", "ugly", "disgusting", "blurry",
            "bad anatomy", "bad proportions", "extra limbs",
            "cloned face", "disfigured", "out of frame", "extra fingers",
            "mutated hands", "poorly drawn hands", "poorly drawn face",
            "mutation", "deformed", "worst quality", "low quality",
            "normal quality", "jpeg artifacts", "signature", "watermark",
            "username", "blurry", "bad feet"
        ],
        "strict": [
            "deformed", "disfigured", "poorly drawn", "extra limbs",
            "cloned face", "gross proportions", "malformed limbs",
            "missing arms", "missing legs", "extra arms", "extra legs",
            "fused fingers", "too many fingers", "long neck",
            "mutation", "mutated", "ugly", "disgusting", "blurry",
            "bad anatomy", "bad proportions", "extra limbs",
            "cloned face", "disfigured", "out of frame", "extra fingers",
            "mutated hands", "poorly drawn hands", "poorly drawn face",
            "mutation", "deformed", "worst quality", "low quality",
            "normal quality", "jpeg artifacts", "signature", "watermark",
            "username", "blurry", "bad feet", "cropped", "poorly drawn",
            "out of frame", "poorly drawn hands", "poorly drawn feet",
            "poorly drawn face", "out of frame", "extra limbs",
            "disfigured", "deformed", "body out of frame", "bad anatomy",
            "watermark", "signature", "cut off", "low contrast",
            "underexposed", "overexposed", "bad art", "beginner",
            "amateur", "grainy", "blurry", "duplicate", "morbid",
            "mutilated", "extra fingers", "mutated hands", "poorly drawn hands",
            "poorly drawn face", "mutation", "deformed", "ugly",
            "blurry", "bad anatomy", "bad proportions", "extra limbs",
            "cloned face", "disfigured", "out of frame", "gross proportions",
            "malformed limbs", "missing arms", "missing legs", "extra arms",
            "extra legs", "mutated hands", "fused fingers", "too many fingers",
            "long neck"
        ]
    }

    num_elements = {
        "basic": (3, 5),
        "standard": (8, 12),
        "strict": (15, 20)
    }

    @classmethod
    def INPUT_TYPES(s):
        all_negatives = list(set([item for sublist in s.negative_elements.values() for item in sublist]))
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "negative_prompt": (all_negatives,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "strictness": (["basic", "standard", "strict"], {"default": "standard"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("negative_prompt", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Enhancement"

    def generate(self, randomize, negative_prompt, seed=0, strictness="standard"):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            min_elements, max_elements = self.num_elements[strictness]
            num_to_select = random.randint(min_elements, max_elements)
            selected_elements = random.sample(self.negative_elements[strictness], num_to_select)
            negative_prompt = ", ".join(selected_elements)
        
        return (negative_prompt, seed) 