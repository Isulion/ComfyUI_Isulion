from ..base_selector import SimpleSelectorNode


class IsulionCuteAnimalRandom(SimpleSelectorNode):
    POOL = [
        'Red Panda', 'Koala', 'Fennec Fox', 'Pygmy Marmoset', 'Quokka', 'Sea Otter', 'Harp Seal Pup', 'Panda Cub', 'Penguin Chick', 'Hedgehog', 'Axolotl', 'Sloth', 'Rabbit', 'Kitten', 'Puppy', 'Meerkat', 'Sugar Glider', 'Chinchilla', 'Slow Loris', 'Hamster', 'Red Fox Kit', 'Lamb', 'Piglet', 'Duckling', 'Pygmy Hippo', 'Baby Giraffe', 'Baby Alpaca', 'Otter Pup', 'Corgi Puppy', 'Golden Retriever Puppy', 'Seal Pup', 'Snow Leopard Cub', 'Tiger Cub', 'Lion Cub', 'Baby Gorilla', 'Baby Orangutan', 'Pygmy Goat', 'Fawn (Baby Deer)', 'Ferret', 'Platypus', 'Kangaroo Joey', 'Wallaby', 'Dik-Dik', 'Serval Kitten', 'Caracal Kitten', 'Clouded Leopard Cub', 'Red Squirrel', 'Chipmunk', 'Prairie Dog', 'Arctic Fox', 'Polar Bear Cub', 'Bottlenose Dolphin Calf', 'Beluga Whale Calf', 'Manatee Calf', 'Baby Skunk', 'Raccoon Kit', 'Baby Opossum', 'Baby Echidna (Puggle)', 'Baby Tapir', 'GiantPanda Cub', 'Baby Hippo', 'Baby Rhino', 'Baby Zebra', 'Baby Elephant Seal', 'Baby Wombat', 'Baby Emu', 'Baby Kiwi Bird', 'Baby Flamingo', 'Cygnet (Baby Swan)', 'Baby Tortoise', 'Baby Alligator', 'Baby Crocodile', 'Baby Chameleon', 'Baby Iguana', 'Baby Frog', 'Baby Toad', 'Baby Gecko', 'Ring-tailed Lemur', 'Sifaka Lemur', 'Mouse Lemur', 'Bush Baby', 'PygmyPossum', 'Baby Mole', 'Baby Bat', 'Leveret (Baby Hare)', 'Baby Mole Rat', 'Baby Porcupine', 'Baby Badger', 'Pygmy Rabbit', 'Baby Seal', 'Baby Puffin', 'Owlet (Baby Owl)', 'Hoglet(Baby Hedgehog)', 'Baby Armadillo', 'Baby Pangolin', 'Baby Okapi', 'Baby Cheetah', 'Baby Ocelot', 'Baby Lynx', 'Baby Tasmanian Devil'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "animal": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "INT",)  # Two outputs: animal string and seed
    RETURN_NAMES = ("animal", "seed",)  # Names for the outputs
    FUNCTION = "random_animal"
    CATEGORY = "Art/Styles"

    def random_animal(self, randomize: str, seed: int, animal: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            # Randomly select from predefined list
            animal = rng.choice(self._pool_for())

        return (f"{animal}", seed)  # Return both the animal name and the seed
