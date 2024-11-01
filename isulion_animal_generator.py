import random
from nodes import NODE_CLASS_MAPPINGS

class IsulionAnimalRandom:
    animals = [
    'Dog','Cat','Horse','Cow','Chicken','Pig','Sheep','Goat','Lion','Tiger','Elephant','Bear','Wolf','Fox','Deer','Rabbit','Kangaroo','Giraffe','Zebra','Monkey','Chimpanzee','Gorilla','Orangutan','Panda','Koala','Hippopotamus','Rhinoceros','Crocodile','Alligator','Eagle','Hawk','Falcon','Owl','Penguin','Dolphin','Whale','Shark','Octopus','Squid','Jellyfish','Crab','Lobster','Clownfish','Sea Turtle','Frog','Toad','Snake','Lizard','Gecko','Tortoise','Camel','Donkey','Bat','Rat','Mouse','Squirrel','Chipmunk','Porcupine','Hedgehog','Skunk','Raccoon','Otter','Seal','Walrus','Polar Bear','Grizzly Bear','Cheetah','Leopard','Jaguar','Antelope','Buffalo','Bison','Moose','Reindeer','Mole','Platypus','Echidna','Parrot','Peacock','Swan','Duck','Goose','Turkey','Flamingo','Pelican','Seagull','Sparrow','Pigeon','Crow','Magpie','Woodpecker','Hummingbird','Butterfly','Bee','Ant','Spider','Scorpion','Worm','Snail','Slug'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "animal": (cls.animals,)
            }
        }

    RETURN_TYPES = ("Animal", "Seed",)  # Two outputs: prompt string and seed
    FUNCTION = "random_animal"
    CATEGORY = "Art/Styles"

    def random_animal(self, randomize, seed, animal):
        if randomize == "enable":
            # Set seed for reproducibility if provided
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            # Randomly select from predefined lists
            animal = random.choice(self.animals)

        return (f"{animal}\n", animal, seed)

# Register the node with ComfyUI
NODE_CLASS_MAPPINGS.update({
    "IsulionAnimalRandom": IsulionAnimalRandom
})
