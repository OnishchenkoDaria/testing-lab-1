from typing import List

from schemas import Point, Line, PairRelation, Result, ResultType
from constants import EPS


# check with the accuracy value (zero check)
def is_zero(z: float) -> bool:
    return abs(z) <= EPS

def line_from_two_points(p1: Point, p2: Point) -> Line:
    # A = y2 - y1, B = x1 - x2, C = x2*y1 - x1*y2
    A = p2.y - p1.y
    B = p1.x - p2.x
    C = p2.x * p1.y - p1.x * p2.y
    # A^2 + B^2 != 0 ensured by validation of distinct points
    return Line(A, B, C)

def line_from_kb(k: int, b: int) -> Line:
    # y = kx + b => kx - y + b = 0
    return Line(float(k), -1.0, float(b))

def det(l1: Line, l2: Line) -> float:
    return l1.A * l2.B - l2.A * l1.B


def are_coincident(l1: Line, l2: Line) -> bool:
    # using parallel check for the coincidence check to avoid division:
    # A1*B2 - A2*B1 = 0  (parallel check)
    return is_zero(l1.A * l2.B - l2.A * l1.B) and \
           is_zero(l1.A * l2.C - l2.A * l1.C) and \
           is_zero(l1.B * l2.C - l2.B * l1.C)


def relate(l1: Line, l2: Line) -> PairRelation:
    d = det(l1, l2)
    if is_zero(d):
        return PairRelation.COINCIDENT if are_coincident(l1, l2) else PairRelation.PARALLEL
    return PairRelation.INTERSECT

def points_equal(p1: Point, p2: Point) -> bool:
    return abs(p1.x - p2.x) <= EPS and abs(p1.y - p2.y) <= EPS

def unique_points(points: List[Point]) -> List[Point]:
    uniq: List[Point] = []
    for p in points:
        if not any(points_equal(p, q) for q in uniq):
            uniq.append(p)
    return uniq

def intersection(l1: Line, l2: Line) -> Point:
    d = det(l1, l2)
    if is_zero(d):
        raise ValueError("Intersection called for parallel/coincident lines (D≈0).")

    x = (l1.B * l2.C - l2.B * l1.C) / d
    y = (l1.C * l2.A - l2.C * l1.A) / d
    return Point(x, y)

def compute_unique_intersections(l1: Line, l2: Line, l3: Line) -> List[Point]:
    pts: List[Point] = []
    for a, b in [(l1, l2), (l1, l3), (l2, l3)]:
        if relate(a, b) == PairRelation.INTERSECT:
            pts.append(intersection(a, b))
    return unique_points(pts)


def classify_three_lines(l1: Line, l2: Line, l3: Line) -> Result:
    r12 = relate(l1, l2)
    r13 = relate(l1, l3)
    r23 = relate(l2, l3)

    # Case 1: all coincident
    if r12 == PairRelation.COINCIDENT and r13 == PairRelation.COINCIDENT and r23 == PairRelation.COINCIDENT:
        return Result(ResultType.ALL_COINCIDENT, ())

    pts = compute_unique_intersections(l1, l2, l3)
    n = len(pts)

    if n == 0:
        return Result(ResultType.NO_INTERSECTIONS, ())
    if n == 1:
        return Result(ResultType.ONE_POINT, (pts[0],))
    if n == 2:
        return Result(ResultType.TWO_POINTS, (pts[0], pts[1]))
    if n == 3:
        return Result(ResultType.THREE_POINTS, (pts[0], pts[1], pts[2]))

    # for three lines on plane this shouldn't happen, but keep safe:
    return Result(ResultType.THREE_POINTS, tuple(pts[:3]))