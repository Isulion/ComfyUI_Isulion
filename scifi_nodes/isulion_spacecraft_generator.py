import random

class IsulionSpacecraftGenerator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "ship_class": ("STRING", {"default": "any"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/SciFi"

    def generate(self, seed=0, ship_class="any"):
        random.seed(seed)
        ships = {
            "military": ["battlecruiser", "stealth frigate", "carrier", "destroyer"],
            "civilian": ["passenger liner", "cargo hauler", "mining vessel", "colony ship"],
            "exploration": ["scout ship", "research vessel", "survey craft", "deep space probe"],
            "special": ["dimensional ship", "time vessel", "living ship", "quantum craft"]
        }
        
        prefixes = ["advanced", "experimental", "prototype", "modified", "enhanced"]
        features = ["with energy shields", "with quantum drive", "with cloaking device", 
                   "with AI core", "with plasma weapons"]
        
        if ship_class != "any" and ship_class in ships:
            base_ship = random.choice(ships[ship_class])
        else:
            all_ships = [ship for sublist in ships.values() for ship in sublist]
            base_ship = random.choice(all_ships)
            
        ship_desc = f"{random.choice(prefixes)} {base_ship} {random.choice(features)}"
        return (ship_desc,) 