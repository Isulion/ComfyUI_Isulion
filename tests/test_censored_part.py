"""Checks for the Isulion Censored Part node."""

from isulion_testkit import import_package, normalize_json


def _censored_part():
    pkg = import_package()
    cls = pkg.NODE_CLASS_MAPPINGS["IsulionCensoredPart"]
    display = pkg.NODE_DISPLAY_NAME_MAPPINGS["IsulionCensoredPart"]
    return cls, display


def test_censored_part_is_registered_with_display_name():
    cls, display = _censored_part()
    assert callable(cls)
    assert "Isulion" in display


def test_censored_part_accepts_image_and_optional_mask():
    cls, _ = _censored_part()
    spec = normalize_json(cls.INPUT_TYPES())
    assert spec["required"]["image"] == ["IMAGE"]
    assert spec["optional"]["mask"] == ["MASK"]


def test_censored_part_offers_irreversible_and_obfuscating_modes():
    cls, _ = _censored_part()
    spec = normalize_json(cls.INPUT_TYPES())
    modes = spec["required"]["censor_mode"][0]
    for expected in ("blur", "pixelate", "pixelate+blur", "black_bar", "noise"):
        assert expected in modes, f"missing censor mode {expected!r}"


def test_censored_part_has_builtin_rectangle_region_selection():
    cls, _ = _censored_part()
    spec = normalize_json(cls.INPUT_TYPES())
    required = spec["required"]
    assert required["use_region_rect"][1]["default"] is False
    for name in ("region_x", "region_y", "region_width", "region_height"):
        widget = required[name][1]
        assert widget["min"] == 0.0 and widget["max"] == 100.0, (
            f"{name} must be percent-based"
        )


def test_censored_part_supports_grow_invert_feather():
    cls, _ = _censored_part()
    spec = normalize_json(cls.INPUT_TYPES())
    grow = spec["required"]["grow_region"][1]
    assert grow["min"] < 0.0 < grow["max"], "grow_region must shrink and enlarge"
    assert spec["required"]["invert_region"][1]["default"] is False
    assert spec["required"]["feather_edge"][1]["min"] == 0.0
    assert spec["required"]["noise_seed"][0] == "INT"


def test_censored_part_strength_sliders_are_percent_based():
    cls, _ = _censored_part()
    spec = normalize_json(cls.INPUT_TYPES())
    for name in ("blur_strength", "pixel_size"):
        widget = spec["required"][name][1]
        assert widget["max"] <= 100.0, f"{name} must stay a percentage"
        assert 0.0 < widget["default"] <= 100.0


def test_censored_part_returns_image_and_censor_mask():
    cls, _ = _censored_part()
    assert tuple(cls.RETURN_TYPES) == ("IMAGE", "MASK")
    assert tuple(cls.RETURN_NAMES) == ("image", "censor_mask")
