"""Checks for the Isulion Space Invaders node (Python side of web/space_invaders.js)."""

import json

from isulion_testkit import import_package


def _node():
    return import_package().NODE_CLASS_MAPPINGS["IsulionSpaceInvaders"]()


def test_space_invaders_reports_saved_scores():
    state = json.dumps({"version": 1, "high_score": 1230, "last_score": 450, "best_wave": 3})
    out = _node().report(state)
    high, last, summary = out["result"]
    assert (high, last) == (1230, 450)
    assert "Best wave: 3" in summary
    assert out["ui"]["summary"] == [summary]


def test_space_invaders_tolerates_bad_state():
    for raw in ("", "not json", "[1, 2]", json.dumps({"high_score": "9999", "last_score": True, "best_wave": -4}),
                '{"high_score": Infinity, "last_score": NaN, "best_wave": 1e999}'):
        high, last, summary = _node().report(raw)["result"]
        assert (high, last) == (0, 0)
        assert "Best wave: 1" in summary
