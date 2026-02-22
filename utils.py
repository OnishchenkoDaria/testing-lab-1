from schemas import Point, Line, PairRelation
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
