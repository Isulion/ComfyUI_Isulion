from ...utils.common import handle_seed, flatten_dict_values

class IsulionPromptEnhancer:
    # ... existing enhancements dictionary ...

    @classmethod
    def INPUT_TYPES(s):
        all_enhancements = [item for focus in s.enhancements.values() 
                          for level in focus.values() 
                          for item in level]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "base_prompt": ("STRING", {"default": ""}),
                "enhancement": (all_enhancements,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "enhancement_level": (["subtle", "moderate", "dramatic"], {"default": "moderate"}),
                "focus": (["detail", "mood", "composition", "lighting", "color"], {"default": "detail"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("enhanced_prompt", "seed",)
    FUNCTION = "enhance"
    CATEGORY = "Isulion/Enhancement"

    def enhance(self, randomize, base_prompt, enhancement, seed=0, enhancement_level="moderate", focus="detail"):
        if randomize == "enable":
            seed = handle_seed(seed)
            enhancement = random.choice(self.enhancements[focus][enhancement_level])
        
        enhanced_prompt = f"{base_prompt}, {enhancement}"
        return (enhanced_prompt, seed) 