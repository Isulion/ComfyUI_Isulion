import random
from nodes import NODE_CLASS_MAPPINGS

class Isulion_ArtStyleGenerator:
    styles = [
        'Realistic', 'Watercolor', 'Oil Painting', 'Sketch', 'Digital Art',
        'Impressionism', 'Expressionism', 'Surrealism', 'Pop Art', 'Abstract',
        'Minimalist', 'Comic Book', 'Manga', 'Anime', 'Pixel Art',
        'Vector Art', 'Low Poly', '3D Rendering', 'Concept Art', 'Fantasy Art',
        'Gothic', 'Baroque', 'Renaissance', 'Art Nouveau', 'Art Deco',
        'Cubism', 'Pointillism', 'Photorealism', 'Hyperrealism', 'Naive Art',
        'Folk Art', 'Street Art', 'Graffiti', 'Retro', 'Vintage',
        'Steampunk', 'Cyberpunk', 'Vaporwave', 'Ukiyo-e', 'Chinese Painting'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "style": (cls.styles,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("style", "seed",)
    FUNCTION = "generate_style"
    CATEGORY = "Art/Styles"

    def generate_style(self, randomize, seed, style):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            style = random.choice(self.styles)

        return (f"{style}", seed)

# Remove NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS from here