"""Factory pattern: a shape factory producing objects with an area() method."""
from __future__ import annotations

import math


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius * self.radius


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return float(self.width * self.height)


class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return float(self.side * self.side)


def _require_positive(name: str, value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a number")
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def make_shape(kind: str, **kwargs: float) -> object:
    """Create a shape object exposing .area() -> float.

    Supported kinds:
        'circle'    -> radius
        'rectangle' -> width, height
        'square'    -> side

    Raises ValueError for an unknown kind or non-positive dimensions.
    """
    if kind == "circle":
        radius = _require_positive("radius", kwargs["radius"])
        return Circle(radius)
    if kind == "rectangle":
        width = _require_positive("width", kwargs["width"])
        height = _require_positive("height", kwargs["height"])
        return Rectangle(width, height)
    if kind == "square":
        side = _require_positive("side", kwargs["side"])
        return Square(side)
    raise ValueError(f"unknown shape kind: {kind!r}")
