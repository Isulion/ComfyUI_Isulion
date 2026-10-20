from ..base_selector import SimpleSelectorNode


class IsulionTechGenerator(SimpleSelectorNode):
    POOLS = {
        "weapons": [
            "plasma rifle", "quantum blade", "sonic cannon", "gravity gun",
            "particle beam", "fusion blaster", "antimatter cannon", "phase disruptor",
            "laser sword", "temporal gun", "void cannon", "energy whip",
            "nano swarm launcher", "dark matter projector", "tachyon emitter"
        ],
        "gadgets": [
            "holographic display", "neural interface", "quantum computer", "teleporter",
            "force field generator", "cloaking device", "matter replicator", "bio scanner",
            "universal translator", "time dilation device", "gravity manipulator", "mind probe",
            "energy shield", "wormhole generator", "quantum entangler"
        ],
        "augments": [
            "cybernetic implant", "nano-enhancer", "bio-mod", "exoskeleton",
            "neural booster", "synthetic organ", "quantum processor", "memory augment",
            "reflex enhancer", "strength amplifier", "sensory upgrade", "stealth system",
            "healing matrix", "combat suite", "energy core"
        ],
        "power": [
            "fusion core", "antimatter reactor", "zero-point module", "quantum battery",
            "dark energy tap", "plasma converter", "neutron source", "void crystal",
            "temporal capacitor", "stellar cell", "dimensional core", "entropy inverter",
            "quantum flux generator", "cosmic energy collector", "singularity engine"
        ]
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "tech": (s._pool_for(),),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "tech_type": (["any", "weapons", "gadgets", "augments", "power"], {"default": "any"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("tech", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, randomize, tech, seed=0, tech_type="any"):
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            tech = rng.choice(self._pool_for(tech_type))

        return (tech, seed)
