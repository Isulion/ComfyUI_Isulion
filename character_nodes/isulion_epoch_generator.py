import random

class IsulionEpochGenerator:
    epochs = [
        "Ancient Egypt", "Ancient Greece", "Roman Empire", "Middle Ages", 
        "Renaissance", "Industrial Revolution", "Victorian Era", "Roaring Twenties",
        "Modern Era", "Digital Age", "Bronze Age", "Iron Age", "Stone Age",
        "Byzantine Empire", "Ming Dynasty", "Edo Period", "Colonial Period",
        "Belle Époque", "Art Deco Period", "Space Age", "Information Age",
        "Medieval Japan", "Viking Age", "Golden Age of Piracy", "Wild West",
        "Prehistoric Times", "Age of Enlightenment", "Age of Exploration",
        "Classical Antiquity", "Dark Ages", "Age of Discovery",
        "Baroque Period", "Gothic Era", "Romantic Period", "Jazz Age",
        "Post-Modern Era", "Cyberpunk Future", "Steampunk Era"
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "epoch": (s.epochs,),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("epoch", "seed",)
    FUNCTION = "generate"
    CATEGORY = "Isulion/Character"

    def generate(self, randomize, epoch, seed=0):
        if randomize == "enable":
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 0xffffffffffffffff)
                random.seed(seed)
            
            epoch = random.choice(self.epochs)
        
        return (epoch, seed)
