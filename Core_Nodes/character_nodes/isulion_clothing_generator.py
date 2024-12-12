import random

class IsulionClothingGenerator:
    clothing = {
        "fantasy": [
            "ornate robes", "leather armor", "silk dress", "royal garments",
            "mage's cloak", "warrior's plate", "peasant's tunic", "noble's attire",
            "dragon scale armor", "elven silk robes", "dwarven battle gear", "wizard's hat",
            "enchanted cloak", "mythril chainmail", "ranger's camouflage", "paladin's armor",
            "druid's vestments", "assassin's garb", "ceremonial robes", "battle mage armor",
            "fairy gossamer dress", "necromancer's robes", "barbarian furs", "royal crown jewels"
        ],
        "modern": [
            "business suit", "casual wear", "formal dress", "streetwear",
            "sporty outfit", "bohemian style", "punk fashion", "minimalist clothing",
            "vintage dress", "designer jeans", "leather jacket", "summer dress",
            "athletic wear", "cocktail dress", "winter coat", "beach wear",
            "office attire", "evening gown", "urban streetwear", "loungewear",
            "hipster fashion", "gothic style", "preppy outfit", "activewear"
        ],
        "sci_fi": [
            "space suit", "cybernetic armor", "holographic clothing", "neon bodysuit",
            "power armor", "anti-gravity boots", "plasma shield wear", "quantum fabric dress",
            "cyborg enhancements", "energy field suit", "stealth camouflage", "bio-luminescent wear",
            "techno-organic suit", "neural interface gear", "phase shift clothing", "zero-g suit"
        ]
    }

    @classmethod
    def INPUT_TYPES(s):
        all_clothing = [item for sublist in s.clothing.values() for item in sublist]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "clothing": (all_clothing,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "style": (["any", "fantasy", "modern", "sci_fi"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("clothing", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, randomize, clothing, seed=0, style="any"):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            if style != "any" and style in self.clothing:
                clothing = random.choice(self.clothing[style])
            else:
                all_clothing = [item for sublist in self.clothing.values() for item in sublist]
                clothing = random.choice(all_clothing)
        
        return (clothing, seed) 