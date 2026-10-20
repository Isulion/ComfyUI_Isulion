from ..base_selector import SimpleSelectorNode


class Isulion_EmotionGenerator(SimpleSelectorNode):
    POOL = [
        'Happy', 'Sad', 'Angry', 'Excited', 'Nervous', 'Calm', 'Peaceful', 'Anxious',
        'Joyful', 'Melancholic', 'Furious', 'Cheerful', 'Depressed', 'Enthusiastic',
        'Frustrated', 'Content', 'Worried', 'Serene', 'Irritated', 'Ecstatic',
        'Gloomy', 'Relaxed', 'Stressed', 'Satisfied', 'Disappointed', 'Proud',
        'Scared', 'Confident', 'Shy', 'Jealous', 'Grateful', 'Lonely', 'Loved',
        'Confused', 'Determined', 'Hopeful', 'Tired', 'Energetic', 'Bored',
        'Surprised', 'Curious', 'Embarrassed', 'Guilty', 'Relief', 'Nostalgic'
    ]
    MAX_SEED = 999999999

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "randomize": (["enable", "disable"],),
                "seed": ("INT", {"default": 0, "min": 0, "max": 999999999}),
                "emotion": (cls.POOL,)
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT",)  # Returns prompt string, emotion, and seed
    RETURN_NAMES = ("prompt", "emotion", "seed",)
    FUNCTION = "generate_emotion"
    CATEGORY = "Art/Styles"

    def generate_emotion(self, randomize: str, seed: int, emotion: str) -> tuple:
        rng, seed = self._make_rng(randomize, seed)

        if randomize == "enable":
            emotion = rng.choice(self._pool_for())

        # Create prompt with the emotion
        prompt = f"feeling {emotion.lower()}, emotional"

        return (prompt, emotion, seed)
