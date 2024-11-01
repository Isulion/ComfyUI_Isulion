from ...utils.common import handle_seed, flatten_dict_values
import random

class IsulionNegativePromptGenerator:
    negative_elements = {
        # ... existing negative_elements dictionary ...
    }

    num_elements = {
        "basic": (3, 5),
        "standard": (8, 12),
        "strict": (15, 20)
    }

    @classmethod
    def INPUT_TYPES(s):
        all_negatives = list(set(flatten_dict_values(s.negative_elements)))
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
            seed = handle_seed(seed)
            
            min_elements, max_elements = self.num_elements[strictness]
            num_to_select = random.randint(min_elements, max_elements)
            selected_elements = random.sample(self.negative_elements[strictness], num_to_select)
            negative_prompt = ", ".join(selected_elements)
        
        return (negative_prompt, seed) 