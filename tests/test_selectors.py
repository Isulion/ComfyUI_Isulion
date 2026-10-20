"""Seeded-selection determinism checks for representative selector nodes.

Covered: Isulion_AnimalRandom, IsulionTechGenerator, Isulion_EmotionGenerator,
IsulionAlienWorldGenerator. All nodes return their (possibly new) seed as the
LAST element of the output tuple.
"""

import random

from isulion_testkit import import_package


def _callers():
    """Per-node callables taking (randomize, seed) -> output tuple."""
    pkg = import_package()
    mappings = pkg.NODE_CLASS_MAPPINGS
    animal = mappings["IsulionAnimalRandom"]()
    tech = mappings["IsulionTechGenerator"]()
    emotion = mappings["IsulionEmotionGenerator"]()
    alien = mappings["IsulionAlienWorldGenerator"]()

    def call_animal(randomize, seed):
        return animal.random_animal(randomize=randomize, seed=seed, animal="Cat")

    def call_tech(randomize, seed):
        return tech.generate(randomize=randomize, tech="quantum blade",
                             seed=seed, tech_type="any")

    def call_emotion(randomize, seed):
        return emotion.generate_emotion(randomize=randomize, seed=seed,
                                        emotion="Happy")

    def call_alien(randomize, seed):
        return alien.generate(randomize=randomize, atmosphere="toxic",
                              terrain="floating islands", color="purple",
                              feature="binary suns", seed=seed)

    return {
        "Isulion_AnimalRandom": call_animal,
        "IsulionTechGenerator": call_tech,
        "Isulion_EmotionGenerator": call_emotion,
        "IsulionAlienWorldGenerator": call_alien,
    }


def _assert_seeded_path_deterministic_and_pollution_free(call):
    # Deterministic across calls with the same seed...
    random.seed(1111)
    first = call("enable", 42)
    random.seed(2222)
    second = call("enable", 42)
    assert first == second
    assert first[-1] == 42
    # ...and unaffected by external global-random pollution.
    random.seed(987654321)
    third = call("enable", 42)
    assert third == first


def _assert_disable_path_passthrough(call, extra_check):
    result = call("disable", 77)
    assert result[-1] == 77, "disable path must return the original seed"
    extra_check(result)


def _assert_fresh_seed_zero_path(call):
    out = call("enable", 0)
    fresh_seed = out[-1]
    assert isinstance(fresh_seed, int) and fresh_seed > 0, (
        f"enable + seed=0 must report a fresh positive seed, got {fresh_seed!r}"
    )
    replay = call("enable", fresh_seed)
    assert replay[:-1] == out[:-1], (
        "replaying the freshly reported seed must reproduce the same choices"
    )


def test_animal_random_seeded_deterministic_and_pollution_free():
    _assert_seeded_path_deterministic_and_pollution_free(
        _callers()["Isulion_AnimalRandom"])


def test_animal_random_disable_returns_dropdown_value_and_original_seed():

    def check(result):
        assert result[0] == "Cat", result

    _assert_disable_path_passthrough(_callers()["Isulion_AnimalRandom"], check)


def test_animal_random_fresh_seed_zero_is_positive_and_self_consistent():
    _assert_fresh_seed_zero_path(_callers()["Isulion_AnimalRandom"])


def test_tech_generator_seeded_deterministic_and_pollution_free():
    _assert_seeded_path_deterministic_and_pollution_free(
        _callers()["IsulionTechGenerator"])


def test_tech_generator_disable_returns_dropdown_value_and_original_seed():

    def check(result):
        assert result[0] == "quantum blade", result

    _assert_disable_path_passthrough(_callers()["IsulionTechGenerator"], check)


def test_tech_generator_fresh_seed_zero_is_positive_and_self_consistent():
    _assert_fresh_seed_zero_path(_callers()["IsulionTechGenerator"])


def test_emotion_generator_seeded_deterministic_and_pollution_free():
    _assert_seeded_path_deterministic_and_pollution_free(
        _callers()["Isulion_EmotionGenerator"])


def test_emotion_generator_disable_keeps_emotion_and_original_seed():

    def check(result):
        prompt, emotion = result[0], result[1]
        assert emotion == "Happy", result
        assert "happy" in prompt, result

    _assert_disable_path_passthrough(_callers()["Isulion_EmotionGenerator"], check)


def test_emotion_generator_fresh_seed_zero_is_positive_and_self_consistent():
    _assert_fresh_seed_zero_path(_callers()["Isulion_EmotionGenerator"])


def test_alien_world_seeded_deterministic_and_pollution_free():
    _assert_seeded_path_deterministic_and_pollution_free(
        _callers()["IsulionAlienWorldGenerator"])


def test_alien_world_disable_composes_dropdown_values_with_original_seed():

    def check(result):
        desc = result[0]
        for fragment in ("toxic", "floating islands", "purple", "binary suns"):
            assert fragment in desc, (fragment, desc)

    _assert_disable_path_passthrough(_callers()["IsulionAlienWorldGenerator"], check)


def test_alien_world_fresh_seed_zero_is_positive_and_self_consistent():
    _assert_fresh_seed_zero_path(_callers()["IsulionAlienWorldGenerator"])
