from ..base_selector import SimpleSelectorNode


class IsulionSpacecraftGenerator(SimpleSelectorNode):
    POOLS = {
        "military": [
            "battlecruiser", "stealth frigate", "carrier", "destroyer",
            "dreadnought", "assault ship", "combat vessel", "strike craft",
            "war barge", "missile frigate", "plasma cruiser", "void hunter",
            "quantum warship", "battle station", "star fortress"
        ],
        "civilian": [
            "passenger liner", "cargo hauler", "mining vessel", "colony ship",
            "space yacht", "trading vessel", "transport ship", "cruise liner",
            "construction ship", "medical frigate", "research vessel", "supply ship",
            "merchant vessel", "repair ship", "salvage craft"
        ],
        "exploration": [
            "scout ship", "research vessel", "survey craft", "deep space probe",
            "pathfinder ship", "expedition craft", "discovery vessel", "stellar explorer",
            "cartographer ship", "science vessel", "observatory ship", "mapping drone",
            "reconnaissance craft", "sensor platform", "probe carrier"
        ],
        "special": [
            "dimensional ship", "time vessel", "living ship", "quantum craft",
            "phase shifter", "void walker", "reality bender", "star seed",
            "consciousness vessel", "dream ship", "infinity craft", "cosmic weaver",
            "paradox jumper", "eternity vessel", "dimension breaker"
        ]
    }

    prefixes = [
        "advanced", "experimental", "prototype", "modified", "enhanced",
        "next-gen", "cutting-edge", "state-of-the-art", "revolutionary",
        "bleeding-edge", "innovative", "custom", "specialized", "elite", "premium"
    ]

    features = [
        "with energy shields", "with quantum drive", "with cloaking device",
        "with AI core", "with plasma weapons", "with temporal stabilizers",
        "with dimensional anchor", "with neural interface", "with antimatter core",
        "with gravity manipulators", "with phase shifters", "with void engines",
        "with reality distortion field", "with consciousness matrix", "with quantum computers"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "ship": (s._pool_for(),),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "ship_class": (["any", "military", "civilian", "exploration", "special"], {"default": "any"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("ship", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, randomize, ship, seed=0, ship_class="any"):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            base_ship = rng.choice(self._pool_for(ship_class))
            ship = f"{rng.choice(self.prefixes)} {base_ship} {rng.choice(self.features)}"

        return (ship, seed)
