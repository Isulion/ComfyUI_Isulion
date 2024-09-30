import random
from nodes import NODE_CLASS_MAPPINGS

class IsulionPromptGenerator:
    styles = [
		'3D Rendering','Abstract Art','Aerial Photography'
    ]

    color_palettes = [
		'Analogous Colors','Autumn Leaves','Black and White'
    ]
    subjects = [
        'A beautiful landscape with rolling hills','A calm lake reflecting the mountains'
    ]
    
    lightings = [
		'Accent Lighting','Ambient Lighting','Artificial Lighting'
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "style": (cls.styles,),
                "subject": ("STRING", {"default": "A beautiful landscape with rolling hills"}),
                "color_palette": (cls.color_palettes,),
                "lighting": (cls.lightings,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)  # Two outputs: prompt string and seed
    FUNCTION = "choose_style_palette_and_lighting"
    CATEGORY = "Art/Styles"

    def choose_style_palette_and_lighting(self, randomize, seed, style, color_palette, lighting, subject):
        if randomize == "enable":
            # If seed is provided and greater than zero, set it for the random generator
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)  # Generate a random seed if none is provided
                random.seed(seed)

            style = random.choice(self.styles)
            color_palette = random.choice(self.color_palettes)
            lighting = random.choice(self.lightings)
            subject = random.choice(self.subjects)

        # Return the prompt and the seed as two separate outputs
        return (f"Subject: {subject}\nStyle: {style}\nColor Palette: {color_palette}\nLighting: {lighting}", seed)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS.update({
    "IsulionPromptGenerator": IsulionPromptGenerator
})
