import random

class IsulionClothingGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "style": ("STRING", {"default": "fantasy"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, seed=0, style="fantasy"):
        random.seed(seed)
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
            ],
            "steampunk": [
                "brass-fitted coat", "Victorian dress with gears", "copper-plated armor",
                "mechanical corset", "clockwork suit", "steam-powered boots", "aviator's gear",
                "brass goggles outfit", "mechanical arm guards", "industrial revolution wear"
            ],
            "historical": [
                "medieval armor", "renaissance dress", "victorian gown", "ancient greek toga",
                "samurai armor", "viking battle gear", "egyptian royal garments", "roman legion armor",
                "celtic warrior outfit", "byzantine robes", "knight's full plate", "noble's doublet",
                "peasant's simple clothes", "merchant's fine garments", "monk's habit", "tribal wear"
            ],
            "cultural": [
                "kimono", "sari", "hanbok", "cheongsam", "lederhosen", "kilt",
                "dashiki", "ao dai", "poncho", "kaftan", "yukata", "dirndl",
                "traditional tribal wear", "ceremonial robes", "folk costume", "festival attire"
            ]
        }
        return (random.choice(clothing.get(style, clothing["fantasy"])),) 