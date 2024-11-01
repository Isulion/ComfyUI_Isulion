import random

class IsulionTechGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "tech_type": ("STRING", {"default": "any"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, seed=0, tech_type="any"):
        random.seed(seed)
        technology = {
            "weapons": ["plasma rifle", "quantum blade", "sonic cannon", "gravity gun"],
            "gadgets": ["holographic display", "neural interface", "quantum computer", "teleporter"],
            "augments": ["cybernetic implant", "nano-enhancer", "bio-mod", "exoskeleton"],
            "power": ["fusion core", "antimatter reactor", "zero-point module", "quantum battery"]
        }
        
        if tech_type != "any" and tech_type in technology:
            return (random.choice(technology[tech_type]),)
            
        all_tech = [item for sublist in technology.values() for item in sublist]
        return (random.choice(all_tech),) 