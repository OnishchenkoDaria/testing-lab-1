from schemas import Point, Result, ResultType


def fmt_point(p: Point) -> str:
    # readable precision
    return f"({p.x:.6f}, {p.y:.6f})"


def print_result(res: Result) -> None:
    if res.kind == ResultType.ALL_COINCIDENT:
        print("Lines coincide")
    elif res.kind == ResultType.NO_INTERSECTIONS:
        print("Lines do not intersect")
    elif res.kind == ResultType.ONE_POINT:
        p = res.points[0]
        print(f"Lines intersect at only point (x0, y0), x0 = {p.x:.6f}, y0 = {p.y:.6f}")
    elif res.kind == ResultType.TWO_POINTS:
        p1, p2 = res.points
        print(f"Two intersection points found (x1, y1) = {fmt_point(p1)}, (x2, y2) = {fmt_point(p2)}")
    elif res.kind == ResultType.THREE_POINTS:
        p1, p2, p3 = res.points
        print(
            "Three intersection points found "
            f"(x1, y1) = {fmt_point(p1)}, (x2, y2) = {fmt_point(p2)}, (x3, y3) = {fmt_point(p3)}"
        )
    else:
        print("Unexpected result type") #fallback
