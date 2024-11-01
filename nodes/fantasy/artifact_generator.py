from ...utils.common import handle_seed, flatten_dict_values

class IsulionArtifactGenerator:
    artifacts = {
        # ... existing artifacts dictionary ...
    }

    @classmethod
    def INPUT_TYPES(s):
        all_artifacts = flatten_dict_values(s.artifacts)
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "artifact": (all_artifacts,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "type": (["any", "weapon", "jewelry", "tool", "relic"], {"default": "any"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("artifact", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Fantasy"

    def generate(self, randomize, artifact, seed=0, type="any"):
        if randomize == "enable":
            seed = handle_seed(seed)
            
            if type != "any" and type in self.artifacts:
                artifact = random.choice(self.artifacts[type])
            else:
                all_artifacts = flatten_dict_values(self.artifacts)
                artifact = random.choice(all_artifacts)
        
        return (artifact, seed) 