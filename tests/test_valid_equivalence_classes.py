import pytest
from schemas import Point, ResultType
from utils import line_from_two_points, line_from_kb, classify_three_lines
from constants import MIN_V as MIN, MAX_V as MAX


# -------------------------
# L1, L2 from points (2), L3 from (5) y=kx+b with b!=0
# use a family y = x + 1 (k=1, b=1) so b != 0 is satisfied.
# -------------------------
@pytest.mark.parametrize("p1,p2", [
    (Point(MIN, MIN + 1), Point(MAX, MAX + 1)),      # boundaries: y=x+1
    (Point(MIN, MIN + 1), Point(MIN + 1, MIN + 2)),  # near left boundary
    (Point(MAX - 1, MAX), Point(MAX, MAX + 1)),      # near right boundary
    (Point(0, 1), Point(10, 11)),                    # mid typical
    (Point(-10, -9), Point(10, 11)),                 # mid wide
    (Point(5, 6), Point(20, 21)),                    # random on y=x+1
])
def test_all_coincident_variant20(p1, p2):
    l1 = line_from_two_points(p1, p2)
    l2 = line_from_two_points(p1, p2)

    # L3 as y = 1*x + 1
    l3 = line_from_kb(1, 1)

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.ALL_COINCIDENT


# -------------------------
# L1: y=x, L2: y=x+1, L3: y=x+2  (all parallel, different)
# b != 0 for L3.
# -------------------------
@pytest.mark.parametrize("shift", [1, 2, 5, 50, -119, 119])
def test_no_intersections_variant20(shift):
    # L1: y = x  (points)
    l1 = line_from_two_points(Point(0, 0), Point(10, 10))

    # L2: y = x + shift (points) -- ensure shift != 0
    l2 = line_from_two_points(Point(0, shift), Point(10, 10 + shift))

    # L3: y = x + (shift + 1) (5) with b != 0
    # if shift == -1 this would make b=0 --- shift set doesn't include -1.
    l3 = line_from_kb(1, shift + 1)

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.NO_INTERSECTIONS


@pytest.mark.parametrize("a,b,c", [
    (1, -1, 2),
    (MIN, MAX, 5),
    (-5, 5, 10),
    (-119, 3, 119),
    (2, 3, 4),
    (10, -20, 30),
])
def test_intersect_one_point(a, b, c):
    # all pass through (0,0)
    l1 = line_from_two_points(Point(0, 0), Point(1, a))
    l2 = line_from_two_points(Point(0, 0), Point(1, b))
    l3 = line_from_two_points(Point(0, 0), Point(1, c))

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.ONE_POINT


@pytest.mark.parametrize("shift", [
    1,
    MIN,
    MAX,
    -119,
    119,
    50,
])
def test_intersect_two_points(shift):
    # l1: y = x
    l1 = line_from_two_points(Point(0, 0), Point(10, 10))

    # l2: y = -x
    l2 = line_from_two_points(Point(0, 0), Point(10, -10))

    # l3: parallel to l1 but shifted
    l3 = line_from_two_points(
        Point(0, shift),
        Point(10, 10 + shift)
    )

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.TWO_POINTS


@pytest.mark.parametrize("shift", [
    1,
    MIN,
    MAX,
    -119,
    119,
    77,
])
def test_three_intersection_points(shift):
    # l1: y = x
    l1 = line_from_two_points(Point(0, 0), Point(10, 10))

    # l2: y = -x
    l2 = line_from_two_points(Point(0, 0), Point(10, -10))

    # l3: horizontal line y = shift
    l3 = line_from_two_points(
        Point(MIN, shift),
        Point(MAX, shift)
    )

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.THREE_POINTS