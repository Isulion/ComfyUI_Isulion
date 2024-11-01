import random

class IsulionActionGenerator:
    actions = [
        "running", "jumping", "fighting", "casting spell", "dancing",
        "flying", "swimming", "climbing", "meditating", "reading",
        "wielding weapon", "performing ritual", "crafting", "sneaking",
        "charging", "defending", "shooting", "aiming", "falling",
        "floating", "levitating", "sprinting", "crouching", "leaping",
        "spinning", "twirling", "marching", "crawling", "balancing",
        "diving", "gliding", "hovering", "kneeling", "posing",
        "reaching", "sitting", "standing", "walking", "writing"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "action": (s.actions,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("action", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Scene"

    def generate(self, randomize, action, seed=0):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            action = random.choice(self.actions)
        
        return (action, seed) 