"""Civitai node output-shape and secret-hygiene regression guards.

With CIVITAI_API_TOKEN unset both API nodes short-circuit to an error message,
which conveniently exercises the full return path without any network access.
"""

import os

from isulion_testkit import import_package

_API_NODE_KEYS = ("IsulionCivitaiModelExplorer", "IsulionCivitaiTrending")


def _instantiate_without_token(key):
    pkg = import_package()
    saved = os.environ.pop("CIVITAI_API_TOKEN", None)
    try:
        # The token is read in __init__, so the env must be clean first.
        return pkg.NODE_CLASS_MAPPINGS[key]()
    finally:
        if saved is not None:
            os.environ["CIVITAI_API_TOKEN"] = saved


def test_search_prompts_returns_tuple_matching_return_types_without_token():
    pkg = import_package()
    explorer = _instantiate_without_token("IsulionCivitaiModelExplorer")
    result = explorer.search_prompts(
        search_query="anime", sort_by="Highest Rated",
        nsfw_filter="Hide NSFW", model_type="All", page=1,
    )
    assert isinstance(result, tuple), type(result)
    assert len(result) == len(pkg.NODE_CLASS_MAPPINGS[
        "IsulionCivitaiModelExplorer"].RETURN_TYPES)
    assert isinstance(result[0], list)


def test_get_trending_returns_tuple_matching_return_types_without_token():
    pkg = import_package()
    trending = _instantiate_without_token("IsulionCivitaiTrending")
    result = trending.get_trending(
        nsfw_filter="Hide NSFW", sort_by="Most Reactions",
        period="Day", number_of_images=1,
    )
    assert isinstance(result, tuple), type(result)
    assert len(result) == len(pkg.NODE_CLASS_MAPPINGS[
        "IsulionCivitaiTrending"].RETURN_TYPES)
    assert isinstance(result[0], list)


def test_input_types_expose_no_api_key_widget():
    pkg = import_package()
    for key in _API_NODE_KEYS:
        spec = pkg.NODE_CLASS_MAPPINGS[key].INPUT_TYPES()
        widgets = set(spec.get("required", {})) | set(spec.get("optional", {}))
        assert "api_key" not in widgets, (
            f"{key} leaks a secret-bearing api_key widget into saved workflows"
        )
