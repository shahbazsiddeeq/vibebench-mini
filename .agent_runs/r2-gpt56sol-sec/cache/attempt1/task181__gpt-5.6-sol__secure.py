"""Shape hierarchy and visitors using double dispatch."""

import math
from typing import Any


def _validate_dimension(value: Any, name: str) -> None:
    """Validate that a dimension is a positive int or float."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a positive int or float")
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


class Circle:
    """A circle with a positive radius."""

    def __init__(self, radius: int | float) -> None:
        _validate_dimension(radius, "radius")
        self.radius = radius

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_circle(self)


class Rectangle:
    """A rectangle with positive width and height."""

    def __init__(self, width: int | float, height: int | float) -> None:
        _validate_dimension(width, "width")
        _validate_dimension(height, "height")
        self.width = width
        self.height = height

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_rectangle(self)


class Square:
    """A square with a positive side length."""

    def __init__(self, side: int | float) -> None:
        _validate_dimension(side, "side")
        self.side = side

    def accept(self, visitor: Any) -> Any:
        return visitor.visit_square(self)


class AreaVisitor:
    """Visitor that calculates shape areas."""

    def visit_circle(self, shape: Circle) -> float:
        return float(math.pi * shape.radius * shape.radius)

    def visit_rectangle(self, shape: Rectangle) -> float:
        return float(shape.width * shape.height)

    def visit_square(self, shape: Square) -> float:
        return float(shape.side * shape.side)


class PerimeterVisitor:
    """Visitor that calculates shape perimeters."""

    def visit_circle(self, shape: Circle) -> float:
        return float(2 * math.pi * shape.radius)

    def visit_rectangle(self, shape: Rectangle) -> float:
        return float(2 * (shape.width + shape.height))

    def visit_square(self, shape: Square) -> float:
        return float(4 * shape.side)


def total_area(shapes: list, visitor: Any) -> float:
    """Return the sum of visitor results for all supplied shapes."""
    required_methods = ("visit_circle", "visit_rectangle", "visit_square")

    try:
        valid_visitor = all(
            callable(getattr(visitor, method)) for method in required_methods
        )
    except (AttributeError, TypeError):
        valid_visitor = False

    if not valid_visitor:
        raise TypeError("visitor must provide all required callable visit methods")

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return float(total)
