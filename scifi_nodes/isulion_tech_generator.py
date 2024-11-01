import random

class IsulionTechGenerator:
    technology = {
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
        all_tech = [item for sublist in s.technology.values() for item in sublist]
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "tech": (all_tech,),
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
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            if tech_type != "any" and tech_type in self.technology:
                tech = random.choice(self.technology[tech_type])
            else:
                all_tech = [item for sublist in self.technology.values() for item in sublist]
                tech = random.choice(all_tech)
        
        return (tech, seed) 