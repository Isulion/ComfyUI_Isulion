"""Registration-level checks for the top-level custom-node package."""

from inspect import getattr_static
from isulion_testkit import import_package, load_fixture


def test_node_class_mappings_keys_match_expected_baseline():
    pkg = import_package()
    expected = sorted(load_fixture("expected_node_keys.json"))
    assert sorted(pkg.NODE_CLASS_MAPPINGS.keys()) == expected


def test_every_mapped_class_exposes_core_comfyui_contract():
    pkg = import_package()
    for name in sorted(pkg.NODE_CLASS_MAPPINGS):
        cls = pkg.NODE_CLASS_MAPPINGS[name]
        for attr in ("INPUT_TYPES", "RETURN_TYPES", "FUNCTION", "CATEGORY"):
            assert hasattr(cls, attr), f"{name} is missing required attribute {attr!r}"
        # INPUT_TYPES must be a classmethod (bound to the class itself).
        assert callable(cls.INPUT_TYPES), f"{name}.INPUT_TYPES is not callable"
        assert getattr(cls.INPUT_TYPES, "__self__", None) is cls, (
            f"{name}.INPUT_TYPES must be a @classmethod (bound to the class)"
        )
        static = getattr_static(cls, "INPUT_TYPES", None)
        assert isinstance(static, classmethod), (
            f"{name}.INPUT_TYPES should be declared with @classmethod"
        )


def test_display_name_mappings_cover_every_registered_node():
    pkg = import_package()
    node_keys = set(pkg.NODE_CLASS_MAPPINGS)
    display_keys = set(pkg.NODE_DISPLAY_NAME_MAPPINGS)
    missing = sorted(node_keys - display_keys)
    assert not missing, (
        "NODE_DISPLAY_NAME_MAPPINGS is missing entries for: "
        f"{missing}"
    )
    extras = sorted(display_keys - node_keys)
    if extras:
        print(f"[warn] display-name entries without a node mapping: {extras}")
