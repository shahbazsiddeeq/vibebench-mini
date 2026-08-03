"""Shape factory implementation."""

from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Any


def _positive_dimension(value: Any, name: str) -> float:
    """Return a validated, finite, positive dimension."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a positive number")

    try:
        dimension = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{name} must be a positive number") from None

    if not math.isfinite(dimension) or dimension <= 0:
        raise ValueError(f"{name} must be a positive number")
    return dimension


def _require_arguments(kwargs: dict[str, Any], expected: set[str]) -> None:
    if set(kwargs) != expected:
        raise ValueError("invalid dimensions for shape")


@dataclass(frozen=True, slots=True)
class Circle:
    radius: float

    def area(self) -> float:
        return math.pi * self.radius * self.radius


@dataclass(frozen=True, slots=True)
class Rectangle:
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True, slots=True)
class Square:
    side: float

    def area(self) -> float:
        return self.side * self.side


def make_shape(kind: str, **kwargs: Any) -> object:
    """Create a shape of the requested kind with validated dimensions."""
    if not isinstance(kind, str):
        raise ValueError("unknown shape kind")

    if kind == "circle":
        _require_arguments(kwargs, {"radius"})
        return Circle(_positive_dimension(kwargs["radius"], "radius"))

    if kind == "rectangle":
        _require_arguments(kwargs, {"width", "height"})
        return Rectangle(
            _positive_dimension(kwargs["width"], "width"),
            _positive_dimension(kwargs["height"], "height"),
        )

    if kind == "square":
        _require_arguments(kwargs, {"side"})
        return Square(_positive_dimension(kwargs["side"], "side"))

    raise ValueError("unknown shape kind")
