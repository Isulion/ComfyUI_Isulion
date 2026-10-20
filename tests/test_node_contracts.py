"""Saved-workflow compatibility guard.

Every node's ``INPUT_TYPES()`` must exactly match the v2 contract snapshot
(``tests/fixtures/node_contracts_v2.json``). The diff against the older v1
baseline (removal of the Civitai ``api_key`` widget) is intentional: secrets
must never be embedded in saved workflows, so v2 is the source of truth.
"""

from isulion_testkit import import_package, load_fixture, normalize_json


def test_input_types_match_v2_contracts_exactly():
    pkg = import_package()
    contracts = load_fixture("node_contracts_v2.json")
    assert set(pkg.NODE_CLASS_MAPPINGS.keys()) == set(contracts.keys()), (
        "node registry and node_contracts_v2.json fixture disagree on key set"
    )

    mismatches = {}
    for name in sorted(contracts):
        cls = pkg.NODE_CLASS_MAPPINGS[name]
        actual = normalize_json(cls.INPUT_TYPES())
        if actual != contracts[name]:
            mismatches[name] = {
                "actual": actual,
                "expected": contracts[name],
            }

    assert not mismatches, (
        "INPUT_TYPES drifted from node_contracts_v2.json for: "
        f"{sorted(mismatches)}\n"
        + "\n".join(
            f"--- {name} ---\n"
            f"actual  : {mismatches[name]['actual']}\n"
            f"expected: {mismatches[name]['expected']}"
            for name in sorted(mismatches)
        )
    )
