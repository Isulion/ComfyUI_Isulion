from ...utils.common import handle_seed, flatten_dict_values
import random

class IsulionSpacecraftGenerator:
    ships = {
        # ... existing ships dictionary ...
    }

    prefixes = [
        # ... existing prefixes list ...
    ]

    features = [
        # ... existing features list ...
    ]

    @classmethod
    def INPUT_TYPES(s):
        all_ships = flatten_dict_values(s.ships)
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "ship": (all_ships,),
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
        if randomize == "enable":
            seed = handle_seed(seed)
            
            if ship_class != "any" and ship_class in self.ships:
                base_ship = random.choice(self.ships[ship_class])
            else:
                all_ships = flatten_dict_values(self.ships)
                base_ship = random.choice(all_ships)
            
            ship = f"{random.choice(self.prefixes)} {base_ship} {random.choice(self.features)}"
        
        return (ship, seed) 