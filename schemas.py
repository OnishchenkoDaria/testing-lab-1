from dataclasses import dataclass
from enum import Enum
from typing import Tuple


@dataclass(frozen=True)
class Point:
    x: float
    y: float

@dataclass(frozen=True)
class Line:
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

# Input Data Schemas

@dataclass(frozen=True)
class Inputs:
    p11: Point
    p12: Point
    p21: Point
    p22: Point
    k: int
    b: int