import random

class Isulion_EmotionGenerator:
    emotions = [
        'Happy', 'Sad', 'Angry', 'Excited', 'Nervous', 'Calm', 'Peaceful', 'Anxious',
        'Joyful', 'Melancholic', 'Furious', 'Cheerful', 'Depressed', 'Enthusiastic',
        'Frustrated', 'Content', 'Worried', 'Serene', 'Irritated', 'Ecstatic',
        'Gloomy', 'Relaxed', 'Stressed', 'Satisfied', 'Disappointed', 'Proud',
        'Scared', 'Confident', 'Shy', 'Jealous', 'Grateful', 'Lonely', 'Loved',
        'Confused', 'Determined', 'Hopeful', 'Tired', 'Energetic', 'Bored',
        'Surprised', 'Curious', 'Embarrassed', 'Guilty', 'Relief', 'Nostalgic'
    ]
  
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "emotion": (cls.emotions,)
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT",)  # Returns prompt string, emotion, and seed
    RETURN_NAMES = ("prompt", "emotion", "seed",)
    FUNCTION = "generate_emotion"
    CATEGORY = "Art/Styles"

    def generate_emotion(self, randomize: str, seed: int, emotion: str) -> tuple:
        if randomize == "enable":
            # Set seed for reproducibility if provided
            if seed is not None and seed > 0:
                random.seed(seed)
            else:
                seed = random.randint(0, 999999999)
                random.seed(seed)

            # Randomly select emotion
            emotion = random.choice(self.emotions)

        # Create prompt with the emotion
        prompt = f"feeling {emotion.lower()}, emotional"
        
        return (prompt, emotion, seed)
