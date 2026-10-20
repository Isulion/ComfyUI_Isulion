from ..base_selector import SimpleSelectorNode


class Isulion_ArtStyleGenerator(SimpleSelectorNode):
    POOL = [
        'Realistic', 'Watercolor', 'Oil Painting', 'Sketch', 'Digital Art',
        'Impressionism', 'Expressionism', 'Surrealism', 'Pop Art', 'Abstract',
        'Minimalist', 'Comic Book', 'Manga', 'Anime', 'Pixel Art',
        'Vector Art', 'Low Poly', '3D Rendering', 'Concept Art', 'Fantasy Art',
        'Gothic', 'Baroque', 'Renaissance', 'Art Nouveau', 'Art Deco',
        'Cubism', 'Pointillism', 'Photorealism', 'Hyperrealism', 'Naive Art',
        'Folk Art', 'Street Art', 'Graffiti', 'Retro', 'Vintage',
        'Steampunk', 'Cyberpunk', 'Vaporwave', 'Ukiyo-e', 'Chinese Painting'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "style": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("style", "seed",)
    FUNCTION = "generate_style"
    CATEGORY = "Art/Styles"

    def generate_style(self, randomize: str, seed: int, style: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            style = rng.choice(self._pool_for())

        return (f"{style}", seed)
