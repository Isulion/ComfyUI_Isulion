import random

class IsulionPromptEnhancer:
    enhancements = {
        "detail": {
            "subtle": ["detailed", "fine", "precise", "clean", "polished", "neat", "crisp", "clear", "defined", "sharp"],
            "moderate": ["highly detailed", "intricate", "elaborate", "refined", "meticulous", "well-defined", "finely crafted", "carefully detailed", "precisely rendered", "expertly detailed"],
            "dramatic": ["extremely detailed", "ultra high detail", "masterfully detailed", "hyper-realistic", "photo-realistic", "incredibly intricate", "exceptionally detailed", "stunningly detailed", "microscopically detailed", "obsessively detailed"]
        },
        "mood": {
            "subtle": ["pleasant", "calm", "gentle", "soft", "peaceful", "serene", "tranquil", "relaxed", "soothing", "mild"],
            "moderate": ["atmospheric", "moody", "emotional", "expressive", "evocative", "poignant", "stirring", "moving", "touching", "sentimental"],
            "dramatic": ["intense", "powerful", "dramatic", "passionate", "overwhelming", "gripping", "electrifying", "heart-wrenching", "soul-stirring", "awe-inspiring"]
        },
        "composition": {
            "subtle": ["balanced", "centered", "harmonious", "structured", "orderly", "symmetrical", "aligned", "measured", "proportioned", "organized"],
            "moderate": ["dynamic", "well-composed", "artistically framed", "professionally shot", "thoughtfully arranged", "skillfully composed", "elegantly framed", "beautifully balanced", "artfully structured", "expertly positioned"],
            "dramatic": ["cinematic", "epic composition", "stunning arrangement", "masterfully composed", "breathtaking composition", "grand scale", "visually striking", "perfectly orchestrated", "magnificently framed", "spectacularly arranged"]
        },
        "lighting": {
            "subtle": ["well-lit", "soft lighting", "natural light", "gentle shadows", "ambient lighting", "diffused light", "even lighting", "balanced lighting", "delicate shadows", "subtle highlights"],
            "moderate": ["dramatic lighting", "professional lighting", "perfect exposure", "beautiful lighting", "artistic lighting", "controlled lighting", "expert illumination", "refined lighting", "sophisticated lighting", "calculated shadows"],
            "dramatic": ["volumetric lighting", "ray tracing", "god rays", "studio lighting", "spectacular illumination", "dynamic light rays", "ethereal glow", "heavenly beams", "brilliant luminescence", "radiant lighting"]
        },
        "color": {
            "subtle": ["colorful", "harmonious colors", "balanced tones", "natural colors", "gentle hues", "soft tones", "muted colors", "understated palette", "delicate tints", "refined shades"],
            "moderate": ["vibrant colors", "rich colors", "beautiful palette", "perfect color balance", "vivid hues", "dynamic colors", "expressive palette", "striking tones", "bold colors", "saturated hues"],
            "dramatic": ["stunning colors", "extreme color contrast", "vivid colors", "spectacular color palette", "extraordinary hues", "intense chromatic range", "dazzling colors", "electrifying palette", "magnificent color harmony", "phenomenal color composition"]
        }
    }

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
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            enhancement = random.choice(self.enhancements[focus][enhancement_level])
        
        enhanced_prompt = f"{base_prompt}, {enhancement}"
        return (enhanced_prompt, seed) 