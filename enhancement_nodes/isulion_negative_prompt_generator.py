import random

class IsulionNegativePromptGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {"default": ""}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "strictness": (["basic", "standard", "strict"], {"default": "standard"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Enhancement"

    def generate(self, positive_prompt, seed=0, strictness="standard"):
        random.seed(seed)
        
        # Common negative elements by category
        negative_elements = {
            "basic": [
                "blurry", "pixelated", "low quality", "watermark",
                "signature", "text", "bad anatomy", "distorted"
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
        
        selected_negatives = negative_elements[strictness]
        # Randomly select a subset of negative elements
        num_elements = {
            "basic": random.randint(3, 5),
            "standard": random.randint(8, 12),
            "strict": random.randint(15, 20)
        }
        
        negative_prompt = ", ".join(random.sample(selected_negatives, num_elements[strictness]))
        
        return (negative_prompt,) 