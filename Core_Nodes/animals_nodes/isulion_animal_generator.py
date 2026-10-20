from ..base_selector import SimpleSelectorNode


class Isulion_AnimalRandom(SimpleSelectorNode):
    POOL = [
        'Dog', 'Cat', 'Horse', 'Cow', 'Chicken', 'Pig', 'Sheep', 'Goat', 'Lion', 'Tiger', 'Elephant', 'Bear', 'Wolf', 'Fox', 'Deer', 'Rabbit', 'Kangaroo', 'Giraffe', 'Zebra', 'Monkey', 'Chimpanzee', 'Gorilla', 'Orangutan', 'Panda', 'Koala', 'Hippopotamus', 'Rhinoceros', 'Crocodile', 'Alligator', 'Eagle', 'Hawk', 'Falcon', 'Owl', 'Penguin', 'Dolphin', 'Whale', 'Shark', 'Octopus', 'Squid', 'Jellyfish', 'Crab', 'Lobster', 'Clownfish', 'Sea Turtle', 'Frog', 'Toad', 'Snake', 'Lizard', 'Gecko', 'Tortoise', 'Camel', 'Donkey', 'Bat', 'Rat', 'Mouse', 'Squirrel', 'Chipmunk', 'Porcupine', 'Hedgehog', 'Skunk', 'Raccoon', 'Otter', 'Seal', 'Walrus', 'Polar Bear', 'Grizzly Bear', 'Cheetah', 'Leopard', 'Jaguar', 'Antelope', 'Buffalo', 'Bison', 'Moose', 'Reindeer', 'Mole', 'Platypus', 'Echidna', 'Parrot', 'Peacock', 'Swan', 'Duck', 'Goose', 'Turkey', 'Flamingo', 'Pelican', 'Seagull', 'Sparrow', 'Pigeon', 'Crow', 'Magpie', 'Woodpecker', 'Hummingbird', 'Butterfly', 'Bee', 'Ant', 'Spider', 'Scorpion', 'Worm', 'Snail', 'Slug'
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
