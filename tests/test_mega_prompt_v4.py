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
