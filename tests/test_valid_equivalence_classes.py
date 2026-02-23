import pytest
from schemas import Point, ResultType
from utils import line_from_two_points, classify_three_lines
from constants import MIN_V as MIN, MAX_V as MAX


@pytest.mark.parametrize("x1,y1,x2,y2", [
    (MIN, MIN, MAX, MAX),          # diagonal through boundaries
    (MIN, 0, MAX, 0),              # horizontal boundary
    (0, MIN, 0, MAX),              # vertical boundary
    (MIN+1, 1, MAX-1, MAX-1),      # near boundaries
    (-10, -10, 10, 10),            # middle diagonal
    (5, 7, 20, 22),                # random
])
def test_all_coincident(x1, y1, x2, y2):
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)

    l1 = line_from_two_points(p1, p2)
    l2 = line_from_two_points(p1, p2)
    l3 = line_from_two_points(p1, p2)

    res = classify_three_lines(l1, l2, l3)
    assert res.kind == ResultType.ALL_COINCIDENT


# parallel
@pytest.mark.parametrize("shift", [
    1,
    5,
    MIN,
    MAX,
    -119,
    50,
])
def test_no_intersections(shift):
    # base line y = x
    p1 = Point(0, 0)
    p2 = Point(10, 10)

    # parallel shifted lines
    p3 = Point(0, shift)
    p4 = Point(10, 10 + shift)

    p5 = Point(0, shift + 5)
    p6 = Point(10, 10 + shift + 5)

    l1 = line_from_two_points(p1, p2)
    l2 = line_from_two_points(p3, p4)
    l3 = line_from_two_points(p5, p6)

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