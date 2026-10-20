from ..base_selector import SimpleSelectorNode


class IsulionAlienWorldGenerator(SimpleSelectorNode):
    atmospheres = [
        "toxic", "breathable", "dense", "thin", "crystalline", "plasma",
        "gaseous", "corrosive", "radioactive", "electromagnetic", "quantum",
        "temporal", "bio-organic", "multi-phasic", "energy-based"
    ]

    terrains = [
        "crystalline desert", "floating islands", "metallic plains", "bio-luminescent jungle",
        "liquid methane ocean", "plasma storms", "geometric mountains", "silicon forests",
        "magnetic fields", "quantum crystals", "living metal", "energy vortexes",
        "gravity wells", "temporal rifts", "phase-shifted landscapes", "void chasms",
        "antimatter lakes", "fractal canyons", "morphic plains", "sentient coral"
    ]

    colors = [
        "purple", "emerald", "crimson", "azure", "golden", "silver",
        "iridescent", "prismatic", "void-black", "plasma-blue", "quantum-white",
        "temporal-green", "nebula-pink", "star-gold", "cosmic-violet"
    ]

    features = [
        "multiple moons", "binary suns", "ring system", "quantum anomalies", "temporal rifts",
        "space elevator", "orbital habitats", "ancient megastructures", "artificial moons",
        "plasma rivers", "crystal spires", "gravity anomalies", "bio-mechanical forests",
        "energy storms", "dimensional portals", "living cities", "floating continents"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "atmosphere": (s.atmospheres,),
                "terrain": (s.terrains,),
                "color": (s.colors,),
                "feature": (s.features,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("world_desc", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, randomize, atmosphere, terrain, color, feature, seed=0):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            atmosphere = rng.choice(self.atmospheres)
            terrain = rng.choice(self.terrains)
            color = rng.choice(self.colors)
            feature = rng.choice(self.features)

        world_desc = f"{color} world with {atmosphere} atmosphere, featuring {terrain} and {feature}"
        return (world_desc, seed)
