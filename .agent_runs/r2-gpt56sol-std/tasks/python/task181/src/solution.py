"""Shape hierarchy and visitors implementing double dispatch."""

from __future__ import annotations

import math
from typing import Any


def _validate_dimension(value: Any, name: str) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{name} must be a positive int or float")
    return value


class Circle:
    def __init__(self, radius: int | float) -> None:
        self.radius = _validate_dimension(radius, "radius")

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_circle(self)


class Rectangle:
    def __init__(self, width: int | float, height: int | float) -> None:
        self.width = _validate_dimension(width, "width")
        self.height = _validate_dimension(height, "height")

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_rectangle(self)


class Square:
    def __init__(self, side: int | float) -> None:
        self.side = _validate_dimension(side, "side")

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_square(self)


class AreaVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return float(math.pi * shape.radius * shape.radius)

    def visit_rectangle(self, shape: Rectangle) -> float:
        return float(shape.width * shape.height)

    def visit_square(self, shape: Square) -> float:
        return float(shape.side * shape.side)


class PerimeterVisitor:
    def visit_circle(self, shape: Circle) -> float:
        return float(2 * math.pi * shape.radius)

    def visit_rectangle(self, shape: Rectangle) -> float:
        return float(2 * (shape.width + shape.height))

    def visit_square(self, shape: Square) -> float:
        return float(4 * shape.side)


def total_area(shapes: list, visitor: Any) -> float:
    required_methods = ("visit_circle", "visit_rectangle", "visit_square")
    if not all(callable(getattr(visitor, method, None)) for method in required_methods):
        raise TypeError("visitor must implement all required visit methods")

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return float(total)
