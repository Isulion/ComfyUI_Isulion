"""Checks for the Isulion Mega Prompt V4 node (Python side of web/mega_prompt_v4.js)."""

import json

from isulion_testkit import import_package


def _mp4():
    import_package()
    from isulion_pkg.Core_Nodes import mega_prompt_v4 as mp4
    return mp4


def test_default_state_shape():
    s = _mp4().default_state()
    assert s["version"] == 1 and s["theme"] == {"name": "", "locked": False}
    assert set(s["reels"]) == {"subject", "location", "style", "effects"}
    assert s["reels"]["location"] == {"text": "", "locked": False, "custom": "", "enabled": True}
    assert "enabled" not in s["reels"]["subject"] and "custom" not in s["reels"]["style"]
    assert (s["complexity"], s["lora"], s["frozen_prompt"]) == ("detailed", "", "")


def test_parse_state_falls_back_on_bad_input():
    mp4 = _mp4()
    for raw in (None, "", "not json", "[1]", '{"version": 2}', '{"version": "1"}', 7):
        assert mp4.parse_state(raw) == mp4.default_state(), raw


def test_parse_state_keeps_valid_fields_and_coerces_bad_ones():
    mp4 = _mp4()
    s = mp4.parse_state(json.dumps({"version": 1, "theme": {"name": "anime", "locked": 1},
        "reels": {"subject": {"text": "hero", "locked": True, "custom": 5},
                  "style": {"enabled": "no", "text": None}},
        "complexity": "epic", "lora": ["x"], "frozen_prompt": "fixed", "junk": 1}))
    assert s["theme"] == {"name": "anime", "locked": False}
    assert s["reels"]["subject"] == {"text": "hero", "locked": True, "custom": ""}
    assert s["reels"]["style"] == {"text": "", "locked": False, "enabled": True}
    assert s["reels"]["location"]["enabled"] is True
    assert (s["complexity"], s["lora"], s["frozen_prompt"]) == ("detailed", "", "fixed")
    assert "junk" not in s
    assert mp4.parse_state(mp4.DEFAULT_STATE) == mp4.default_state()


def test_theme_entry_and_list_themes():
    mp4 = _mp4()
    assert mp4.theme_entry("anime") == {"name": "anime", "display": "🎌 Anime", "icon": "🎌", "label": "Anime"}
    assert mp4.theme_entry("nope") == {"name": "nope", "display": "nope", "icon": "🎰", "label": "nope"}
    themes = mp4.list_themes()
    names = [t["name"] for t in themes]
    assert "random" not in names and "anime" in names and len(names) == len(set(names))
    assert [t["label"] for t in themes] == sorted(t["label"] for t in themes)


def _state(**over):
    mp4 = _mp4()
    s = mp4.default_state()
    s["reels"]["subject"]["text"] = "a hero, ((masterpiece))"
    s["reels"]["location"]["text"] = "in a forest"
    s["reels"]["style"]["text"] = "oil painting"
    s["reels"]["effects"]["text"] = "glowing embers"
    for k, v in over.items():
        s[k] = v
    return s


def test_assemble_order_complexity_and_lora():
    mp4 = _mp4()
    s = _state(lora="  <lora:jade:0.8> ")
    prompt, segs = mp4.assemble_prompt(s)
    assert [x["reel"] for x in segs] == ["subject", "location", "style", "effects", "complexity", "lora"]
    assert prompt == "a hero, ((masterpiece)), in a forest, oil painting, glowing embers, highly detailed, sharp focus, <lora:jade:0.8>"
    assert prompt.endswith("<lora:jade:0.8>")


def test_assemble_disabled_reel_is_absent():
    mp4 = _mp4()
    s = _state()
    s["reels"]["style"]["enabled"] = False
    prompt, segs = mp4.assemble_prompt(s)
    assert "oil painting" not in prompt and "style" not in [x["reel"] for x in segs]


def test_assemble_simple_keeps_custom_text_chunks():
    mp4 = _mp4()
    s = _state(complexity="simple")
    s["reels"]["subject"]["text"] = "my elf queen, ((8k)), (queen of 8 kingdoms)"
    prompt, segs = mp4.assemble_prompt(s)
    assert segs[0]["text"] == "my elf queen, (queen of 8 kingdoms)"
    assert "complexity" not in [x["reel"] for x in segs]


def test_assemble_complex_and_dedup():
    mp4 = _mp4()
    s = _state(complexity="complex")
    s["reels"]["effects"]["text"] = "Oil Painting"
    prompt, segs = mp4.assemble_prompt(s)
    assert prompt.count("il painting") == 1 and prompt.endswith("masterpiece")


def test_assemble_frozen_prompt_wins():
    mp4 = _mp4()
    prompt, segs = mp4.assemble_prompt(_state(frozen_prompt="exactly this", lora="x"))
    assert prompt == "exactly this" and segs == [{"reel": "frozen", "text": "exactly this"}]


import random
import types


class _Handler:
    DISPLAY_NAME = "🧪 Alpha"

    def __init__(self, fail=False):
        self.calls, self.fail = [], fail

    def generate(self, **kw):
        self.calls.append(kw)
        if self.fail:
            raise KeyError("anime.characters")
        n = len(self.calls)
        return {"subject": f"subject {kw['custom_subject'] or n}", "environment": f"env {kw['custom_location'] or n}",
                "style": f"style {n}", "effects": f"fx {n}"}


def _registry(fail=False):
    h = _Handler(fail)
    cm = types.SimpleNamespace(random=random.Random(), seeds=[])
    cm.set_seed = cm.seeds.append
    return types.SimpleNamespace(handlers={"alpha": h, "beta": _Handler()}, config_manager=cm), h


def test_roll_same_seed_same_result_with_real_registry():
    mp4 = _mp4()
    s = mp4.default_state()
    s["theme"] = {"name": "anime", "locked": True}
    a, b = mp4.roll(s, mp4.REEL_NAMES, 42), mp4.roll(s, mp4.REEL_NAMES, 42)
    assert a == b and a["prompt"] and a["seed"] == 42 and a["theme"]["name"] == "anime"
    assert a["state"]["theme"]["name"] == "anime" and "theme" not in a["rolled"]
    assert mp4.roll(s, mp4.REEL_NAMES, 43)["prompt"] != a["prompt"]


def test_roll_never_touches_locked_reels_and_only_requested_ones():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state()
    s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["subject"].update(text="KEEP ME", locked=True)
    s["reels"]["style"]["text"] = "old style"
    out = mp4.roll(s, ["subject", "location"], 1, registry=reg)
    r = out["state"]["reels"]
    assert r["subject"]["text"] == "KEEP ME" and r["style"]["text"] == "old style"
    assert r["location"]["text"] == "env 1" and out["rolled"] == ["location"]
    assert reg.config_manager.seeds == [1] and h.calls[0]["include_style"] is True
    assert s["reels"]["location"]["text"] == ""  # input not mutated


def test_roll_unlocked_theme_is_random_and_recorded():
    mp4 = _mp4()
    reg, _ = _registry()
    s = mp4.default_state()
    out = mp4.roll(s, mp4.REEL_NAMES, 7, registry=reg)
    assert out["state"]["theme"]["name"] in ("alpha", "beta") and "theme" in out["rolled"]
    assert out["theme"]["icon"] == "🧪"


def test_roll_unknown_theme_falls_back_to_random():
    mp4 = _mp4()
    reg, _ = _registry()
    s = mp4.default_state()
    s["theme"] = {"name": "gone", "locked": True}
    out = mp4.roll(s, ["style"], 3, registry=reg)
    assert out["state"]["theme"]["name"] in ("alpha", "beta") and out["prompt"]


def test_roll_pinned_custom_text_is_passed_to_handler():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state()
    s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["subject"]["custom"] = "my elf queen"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert h.calls[0]["custom_subject"] == "my elf queen"
    assert out["state"]["reels"]["subject"]["text"] == "subject my elf queen"


def test_roll_disabled_reel_keeps_text_then_fills_when_enabled():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state()
    s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["location"]["enabled"] = False
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["state"]["reels"]["location"]["text"] == "" and "location" not in out["rolled"]
    assert h.calls[0]["include_environment"] is False and "env" not in out["prompt"]
    s2 = out["state"]
    s2["reels"]["location"]["enabled"] = True
    assert mp4.roll(s2, ["location"], 2, registry=reg)["state"]["reels"]["location"]["text"] == "env 2"


def test_roll_frozen_prompt_skips_handlers():
    mp4 = _mp4()
    reg, h = _registry()
    s = mp4.default_state()
    s["frozen_prompt"] = "fixed"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["prompt"] == "fixed" and out["rolled"] == [] and h.calls == []


def test_roll_handler_exception_returns_error_prompt():
    mp4 = _mp4()
    reg, _ = _registry(fail=True)
    s = mp4.default_state()
    s["theme"] = {"name": "alpha", "locked": True}
    s["reels"]["style"]["text"] = "old"
    out = mp4.roll(s, mp4.REEL_NAMES, 1, registry=reg)
    assert out["prompt"].startswith("Error: KeyError") and out["segments"][0]["reel"] == "error"
    assert out["state"]["reels"]["style"]["text"] == "old" and out["rolled"] == []


def test_roll_uses_the_shared_generation_lock():
    mp4 = _mp4()

    class RecordingLock:
        entries = 0
        def __enter__(self): RecordingLock.entries += 1
        def __exit__(self, *a): return False

    reg, _ = _registry()
    original, mp4.GENERATION_LOCK = mp4.GENERATION_LOCK, RecordingLock()
    try:
        mp4.roll(mp4.default_state(), mp4.REEL_NAMES, 1, registry=reg)
        assert RecordingLock.entries == 1
    finally:
        mp4.GENERATION_LOCK = original
