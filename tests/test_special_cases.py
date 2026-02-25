import pytest
import utils
from schemas import Point, ResultType


# -------------------------
# L1: y = x
# L2: y = x + 1  (parallel)
# L3: y = x + 2  (parallel (5))
# intersection() must NOT be called (D = 0 cases only)
# -------------------------
def test_parallel_does_not_call_intersection(monkeypatch):

    calls = {"n": 0}

    def spy_intersection(l1, l2):
        calls["n"] += 1
        return utils.intersection(l1, l2)

    monkeypatch.setattr(utils, "intersection", spy_intersection)

    l1 = utils.line_from_two_points(Point(0, 0), Point(10, 10))
    l2 = utils.line_from_two_points(Point(0, 1), Point(10, 11))
    l3 = utils.line_from_kb(1, 2)

    res = utils.classify_three_lines(l1, l2, l3)

    assert res.kind == ResultType.NO_INTERSECTIONS
    assert calls["n"] == 0

# -------------------------
# L1, L2 from points on y = x + 1
# L3 from (5): y = 1*x + 1
# lines coincide, intersection() must NOT be called -- unnecessary computations
# -------------------------
def test_all_coincident_no_intersection_call(monkeypatch):

    calls = {"n": 0}

    def spy_intersection(l1, l2):
        calls["n"] += 1
        return utils.intersection(l1, l2)

    monkeypatch.setattr(utils, "intersection", spy_intersection)

    l1 = utils.line_from_two_points(Point(0, 1), Point(10, 11))
    l2 = utils.line_from_two_points(Point(-10, -9), Point(10, 11))
    l3 = utils.line_from_kb(1, 1)

    res = utils.classify_three_lines(l1, l2, l3)

    assert res.kind == ResultType.ALL_COINCIDENT
    assert calls["n"] == 0

# -------------------------
# L1 == L2 : y = x + 1
# L3: y = 5  (k=0, b=5)
# one unique intersection -- intersection() must be called at most once
# -------------------------
def test_two_coincident_one_intersection_call(monkeypatch):

    calls = {"n": 0}
    real_intersection = utils.intersection

    def spy_intersection(l1, l2):
        calls["n"] += 1
        return real_intersection(l1, l2)

    monkeypatch.setattr(utils, "intersection", spy_intersection)

    l1 = utils.line_from_two_points(Point(0, 1), Point(10, 11))
    l2 = utils.line_from_two_points(Point(-10, -9), Point(10, 11))
    l3 = utils.line_from_kb(0, 5)

    res = utils.classify_three_lines(l1, l2, l3)

    assert res.kind == ResultType.ONE_POINT
    assert calls["n"] <= 1