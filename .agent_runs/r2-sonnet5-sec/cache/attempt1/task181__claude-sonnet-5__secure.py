"""
Shape Visitor (Double Dispatch) implementation.

This module defines a small shape hierarchy (Circle, Rectangle, Square)
and concrete visitors (AreaVisitor, PerimeterVisitor) implementing the
Visitor design pattern with double dispatch. Input validation is strict:
all dimensions must be real numbers (int or float, excluding bool) and
strictly positive.
"""

import math
from abc import ABC, abstractmethod
from typing import List


def _validate_positive_number(value, name: str) -> float:
    """
    Validate that `value` is an int or float (not bool) and strictly positive.

    Raises:
        ValueError: if the value is not a valid positive number.

    Returns:
        The value converted to float.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be an int or float, not bool or other type")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0")
    return float(value)


class Shape(ABC):
    """Abstract base class for all shapes."""

    @abstractmethod
    def accept(self, visitor):
        """Dispatch to the appropriate visitor method."""
        raise NotImplementedError


class Circle(Shape):
    """A circle defined by its radius."""

    def __init__(self, radius):
        self.radius = _validate_positive_number(radius, "radius")

    def accept(self, visitor):
        return visitor.visit_circle(self)


class Rectangle(Shape):
    """A rectangle defined by its width and height."""

    def __init__(self, width, height):
        self.width = _validate_positive_number(width, "width")
        self.height = _validate_positive_number(height, "height")

    def accept(self, visitor):
        return visitor.visit_rectangle(self)


class Square(Shape):
    """A square defined by its side length."""

    def __init__(self, side):
        self.side = _validate_positive_number(side, "side")

    def accept(self, visitor):
        return visitor.visit_square(self)


class ShapeVisitor(ABC):
    """Abstract base class for shape visitors."""

    @abstractmethod
    def visit_circle(self, circle: Circle) -> float:
        raise NotImplementedError

    @abstractmethod
    def visit_rectangle(self, rectangle: Rectangle) -> float:
        raise NotImplementedError

    @abstractmethod
    def visit_square(self, square: Square) -> float:
        raise NotImplementedError


class AreaVisitor(ShapeVisitor):
    """Visitor that computes the area of a shape."""

    def visit_circle(self, circle: Circle) -> float:
        return float(math.pi * circle.radius * circle.radius)

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return float(rectangle.width * rectangle.height)

    def visit_square(self, square: Square) -> float:
        return float(square.side * square.side)


class PerimeterVisitor(ShapeVisitor):
    """Visitor that computes the perimeter of a shape."""

    def visit_circle(self, circle: Circle) -> float:
        return float(2 * math.pi * circle.radius)

    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return float(2 * (rectangle.width + rectangle.height))

    def visit_square(self, square: Square) -> float:
        return float(4 * square.side)


def total_area(shapes: List[Shape], visitor) -> float:
    """
    Compute the sum of shape.accept(visitor) over all shapes.

    Raises:
        TypeError: if visitor lacks any of visit_circle, visit_rectangle,
            visit_square as callable attributes.

    Returns:
        The total as a float.
    """
    required_methods = ("visit_circle", "visit_rectangle", "visit_square")
    for method_name in required_methods:
        method = getattr(visitor, method_name, None)
        if not callable(method):
            raise TypeError(
                f"visitor must implement a callable '{method_name}' method"
            )

    total = 0.0
    for shape in shapes:
        total += shape.accept(visitor)
    return float(total)
