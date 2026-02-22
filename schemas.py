from dataclasses import dataclass


@dataclass
class Point (frozen=True):
    x: float
    y: float

@dataclass
class Line(frozen=True):
    A: float
    B: float
    C: float
