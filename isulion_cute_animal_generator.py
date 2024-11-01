import random
from nodes import NODE_CLASS_MAPPINGS

class IsulionCuteAnimalRandom:
    animals = [
		'Red Panda','Koala','Fennec Fox','Pygmy Marmoset','Quokka','Sea Otter','Harp Seal Pup','Panda Cub','Penguin Chick','Hedgehog','Axolotl','Sloth','Rabbit','Kitten','Puppy','Meerkat','Sugar Glider','Chinchilla','Slow Loris','Hamster','Red Fox Kit','Lamb','Piglet','Duckling','Pygmy Hippo','Baby Giraffe','Baby Alpaca','Otter Pup','Corgi Puppy','Golden Retriever Puppy','Seal Pup','Snow Leopard Cub','Tiger Cub','Lion Cub','Baby Gorilla','Baby Orangutan','Pygmy Goat','Fawn (Baby Deer)','Ferret','Platypus','Kangaroo Joey','Wallaby','Dik-Dik','Serval Kitten','Caracal Kitten','Clouded Leopard Cub','Red Squirrel','Chipmunk','Prairie Dog','Arctic Fox','Polar Bear Cub','Bottlenose Dolphin Calf','Beluga Whale Calf','Manatee Calf','Baby Skunk','Raccoon Kit','Baby Opossum','Baby Echidna (Puggle)','Baby Tapir','GiantPanda Cub','Baby Hippo','Baby Rhino','Baby Zebra','Baby Elephant Seal','Baby Wombat','Baby Emu','Baby Kiwi Bird','Baby Flamingo','Cygnet (Baby Swan)','Baby Tortoise','Baby Alligator','Baby Crocodile','Baby Chameleon','Baby Iguana','Baby Frog','Baby Toad','Baby Gecko','Ring-tailed Lemur','Sifaka Lemur','Mouse Lemur','Bush Baby','PygmyPossum','Baby Mole','Baby Bat','Leveret (Baby Hare)','Baby Mole Rat','Baby Porcupine','Baby Badger','Pygmy Rabbit','Baby Seal','Baby Puffin','Owlet (Baby Owl)','Hoglet(Baby Hedgehog)','Baby Armadillo','Baby Pangolin','Baby Okapi','Baby Cheetah','Baby Ocelot','Baby Lynx','Baby Tasmanian Devil'
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
    "IsulionCuteAnimalRandom": IsulionCuteAnimalRandom
})
