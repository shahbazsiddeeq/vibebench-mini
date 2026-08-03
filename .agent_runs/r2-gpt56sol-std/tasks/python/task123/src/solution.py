import math
from dataclasses import dataclass
from numbers import Real
from typing import Any


def _positive_dimension(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a positive number")

    dimension = float(value)
    if not math.isfinite(dimension) or dimension <= 0:
        raise ValueError(f"{name} must be a positive number")
    return dimension


@dataclass(frozen=True)
class Circle:
    radius: float

    def area(self) -> float:
        return math.pi * self.radius ** 2


@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True)
class Square:
    side: float

    def area(self) -> float:
        return self.side ** 2


def make_shape(kind: str, **kwargs: Any) -> object:
    required_parameters = {
        "circle": ("radius",),
        "rectangle": ("width", "height"),
        "square": ("side",),
    }

    if kind not in required_parameters:
        raise ValueError(f"Unknown shape kind: {kind!r}")

    required = required_parameters[kind]
    if set(kwargs) != set(required):
        raise ValueError(
            f"{kind} requires exactly these dimensions: {', '.join(required)}"
        )

    dimensions = {
        name: _positive_dimension(name, kwargs[name])
        for name in required
    }

    if kind == "circle":
        return Circle(dimensions["radius"])
    if kind == "rectangle":
        return Rectangle(dimensions["width"], dimensions["height"])
    return Square(dimensions["side"])
