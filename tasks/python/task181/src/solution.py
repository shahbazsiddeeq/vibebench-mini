from __future__ import annotations

import math


def _check_dim(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return float(value)


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = _check_dim(radius, "radius")

    def accept(self, visitor: object):
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = _check_dim(width, "width")
        self.height = _check_dim(height, "height")

    def accept(self, visitor: object):
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side: float) -> None:
        self.side = _check_dim(side, "side")

    def accept(self, visitor: object):
        return visitor.visit_square(self)


class AreaVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return math.pi * shape.radius * shape.radius

    def visit_rectangle(self, shape: Rectangle) -> float:
        return shape.width * shape.height

    def visit_square(self, shape: Square) -> float:
        return shape.side * shape.side


class PerimeterVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return 2.0 * math.pi * shape.radius

    def visit_rectangle(self, shape: Rectangle) -> float:
        return 2.0 * (shape.width + shape.height)

    def visit_square(self, shape: Square) -> float:
        return 4.0 * shape.side


def total_area(shapes: list, visitor: object) -> float:
    for method in ("visit_circle", "visit_rectangle", "visit_square"):
        if not callable(getattr(visitor, method, None)):
            raise TypeError(f"visitor missing {method}")
    return sum(shape.accept(visitor) for shape in shapes)
