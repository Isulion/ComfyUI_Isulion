import json
import math

DEFAULT_STATE = '{"version": 1, "high_score": 0, "last_score": 0, "best_wave": 1}'


def parse_game_state(raw):
    """Read the JSON written by the browser game; bad or missing data falls back to zeros."""
    try:
        data = json.loads(raw or "{}")
    except (TypeError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}

    def as_int(key, default):
        value = data.get(key, default)
        # bool is a subclass of int: reject it explicitly
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return default
        if isinstance(value, float) and not math.isfinite(value):  # json.loads accepts NaN/Infinity
            return default
        return max(0, int(value))

    return {
        "high_score": as_int("high_score", 0),
        "last_score": as_int("last_score", 0),
        "best_wave": max(1, as_int("best_wave", 1)),
    }


class IsulionSpaceInvaders:
    """
    A small Space Invaders game played inside the node (see web/space_invaders.js).
    The browser stores scores in the hidden ``game_state`` widget; executing the
    node outputs them, so a session's best score can feed a prompt or a seed.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "game_state": ("STRING", {"default": DEFAULT_STATE}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("high_score", "last_score", "summary")
    FUNCTION = "report"
    CATEGORY = "Isulion/Games"
    OUTPUT_NODE = True

    def report(self, game_state):
        state = parse_game_state(game_state)
        summary = (
            f"High score: {state['high_score']} | Last score: {state['last_score']} "
            f"| Best wave: {state['best_wave']}"
        )
        return {
            "ui": {"summary": [summary]},
            "result": (state["high_score"], state["last_score"], summary),
        }
