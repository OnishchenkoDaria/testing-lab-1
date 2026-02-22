from dataclasses import dataclass
from enum import Enum
from typing import Tuple


@dataclass
class Point (frozen=True):
    x: float
    y: float

@dataclass
class Line(frozen=True):
    A: float
    B: float
    C: float

# Output Results schemas

class PairRelation(Enum):
    COINCIDENT = "Coincident"
    PARALLEL = "Parallel"
    INTERSECT = "Intersect"


class ResultType(Enum):
    ALL_COINCIDENT = "AllCoincident"
    NO_INTERSECTIONS = "NoIntersections"
    ONE_POINT = "OnePoint"
    TWO_POINTS = "TwoPoints"
    THREE_POINTS = "ThreePoints"


@dataclass(frozen=True)
class Result:
    kind: ResultType
    points: Tuple[Point, ...] = ()