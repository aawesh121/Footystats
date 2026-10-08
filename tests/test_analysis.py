import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import analysis


def rows():
    return [
        {"season": "20/21", "matches": 30, "goals": 10, "assists": 5, "minutes": 2700},
        {"season": "20/21", "matches": 5, "goals": 2, "assists": 0, "minutes": 450},
        {"season": "21/22", "matches": 34, "goals": 20, "assists": 8, "minutes": 3000},
    ]


def test_per90():
    assert analysis.per90(9, 900) == 0.9
    assert analysis.per90(5, 0) == 0.0


def test_summarize_totals():
    s = analysis.summarize(rows())
    assert s["goals"] == 32
    assert s["assists"] == 13
    assert s["contributions"] == 45
    assert s["best_season"] == "21/22"


def test_empty():
    s = analysis.summarize([])
    assert s["goals"] == 0 and s["best_season"] is None
