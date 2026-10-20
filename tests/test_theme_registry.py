"""Theme registry, singleton behaviour and MegaPromptV3 determinism checks."""

from isulion_testkit import import_package, load_fixture


def _mega_prompt_v3():
    pkg = import_package()
    from isulion_pkg.Core_Nodes.mega_prompt_V3 import IsulionMegaPromptV3

    return pkg, IsulionMegaPromptV3()


def test_theme_mappings_match_display_name_fixture_exactly():
    import_package()
    from isulion_pkg.Core_Nodes.configs.config_manager import ConfigManager
    from isulion_pkg.Core_Nodes.mega_prompt_V3 import ThemeRegistry

    registry = ThemeRegistry(ConfigManager())
    expected = load_fixture("theme_display_names.json")
    assert registry.theme_mappings == expected


def test_get_theme_registry_is_a_singleton():
    import_package()
    from isulion_pkg.Core_Nodes.mega_prompt_V3 import get_theme_registry

    assert get_theme_registry() is get_theme_registry()


ANIME_THEME = "🎌 Anime"


def test_generate_with_randomize_enable_and_seed_is_deterministic():
    _, node = _mega_prompt_v3()
    kwargs = dict(complexity="detailed", randomize="enable", seed=42)
    out_a = node.generate(theme=ANIME_THEME, **kwargs)
    out_b = node.generate(theme=ANIME_THEME, **kwargs)
    assert len(out_a) == 7
    assert out_a == out_b
    assert out_a[-1] == 42


def test_generate_with_randomize_disable_is_deterministic_and_keeps_seed():
    _, node = _mega_prompt_v3()
    kwargs = dict(complexity="detailed", randomize="disable", seed=0)
    out_a = node.generate(theme=ANIME_THEME, **kwargs)
    out_b = node.generate(theme=ANIME_THEME, **kwargs)
    assert len(out_a) == 7
    assert out_a == out_b
    assert out_a[-1] == 0


def test_generate_with_error_theme_returns_error_tuple_without_raising():
    _, node = _mega_prompt_v3()
    result = node.generate(theme="--- Error ---")
    assert len(result) == 7
    prompt, selected_theme = result[0], result[1]
    assert isinstance(prompt, str)
    assert "error" in prompt.lower() or "failed" in prompt.lower()
    assert selected_theme == "--- Error ---"
