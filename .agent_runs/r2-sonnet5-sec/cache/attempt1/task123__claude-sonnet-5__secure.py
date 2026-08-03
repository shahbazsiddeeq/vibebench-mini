"""
Factory Pattern (Shape Factory)

A small, security-conscious module that provides a `make_shape` factory
function for constructing simple geometric shape objects. Each returned
object exposes an `.area() -> float` method.

Design goals:
- No use of eval/exec or dynamic code execution.
- Strict validation of all inputs (types and values).
- No I/O, no printing, no external data sources.
- Clear, non-leaky error messages (ValueError) for invalid input.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from numbers import Real
from typing import Any, Dict


class Shape(ABC):
    """Abstract base class for all shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape as a float."""
        raise NotImplementedError


def _validate_positive_number(value: Any, name: str) -> float:
    """
    Validate that `value` is a real number (int/float, not bool) and strictly
    positive. Returns the value converted to float.

    Raises:
        ValueError: if the value is not a valid positive real number.
    """
    # Explicitly reject booleans, since bool is a subclass of int.
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"Invalid value for '{name}': must be a real number")

    numeric_value = float(value)

    if not math.isfinite(numeric_value):
        raise ValueError(f"Invalid value for '{name}': must be finite")

    if numeric_value <= 0:
        raise ValueError(f"Invalid value for '{name}': must be positive")

    return numeric_value


class Circle(Shape):
    """A circle defined by its radius."""

    __slots__ = ("_radius",)

    def __init__(self, radius: float) -> None:
        self._radius = _validate_positive_number(radius, "radius")

    def area(self) -> float:
        return math.pi * self._radius ** 2


class Rectangle(Shape):
    """A rectangle defined by width and height."""

    __slots__ = ("_width", "_height")

    def __init__(self, width: float, height: float) -> None:
        self._width = _validate_positive_number(width, "width")
        self._height = _validate_positive_number(height, "height")

    def area(self) -> float:
        return self._width * self._height


class Square(Shape):
    """A square defined by its side length."""

    __slots__ = ("_side",)

    def __init__(self, side: float) -> None:
        self._side = _validate_positive_number(side, "side")

    def area(self) -> float:
        return self._side ** 2


# Registry mapping shape kind -> (constructor, required parameter names)
_SHAPE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "circle": {"cls": Circle, "params": ("radius",)},
    "rectangle": {"cls": Rectangle, "params": ("width", "height")},
    "square": {"cls": Square, "params": ("side",)},
}


def make_shape(kind: str, **kwargs: Any) -> Shape:
    """
    Factory function that creates a shape instance based on `kind`.

    Args:
        kind: One of 'circle', 'rectangle', 'square'.
        **kwargs: Shape-specific dimension arguments:
            - circle: radius
            - rectangle: width, height
            - square: side

    Returns:
        An object implementing `.area() -> float`.

    Raises:
        ValueError: If `kind` is unknown, required parameters are missing,
                    extra/unexpected parameters are supplied, or any
                    dimension is not a positive finite real number.
    """
    if not isinstance(kind, str):
        raise ValueError("Invalid shape kind: must be a string")

    normalized_kind = kind.strip().lower()

    entry = _SHAPE_REGISTRY.get(normalized_kind)
    if entry is None:
        raise ValueError(f"Unknown shape kind: '{kind}'")

    expected_params = entry["params"]
    cls = entry["cls"]

    # Reject unexpected keyword arguments to avoid silent misuse.
    unexpected = set(kwargs.keys()) - set(expected_params)
    if unexpected:
        raise ValueError(
            f"Unexpected argument(s) for shape '{normalized_kind}': "
            f"{', '.join(sorted(unexpected))}"
        )

    missing = [p for p in expected_params if p not in kwargs]
    if missing:
        raise ValueError(
            f"Missing required argument(s) for shape '{normalized_kind}': "
            f"{', '.join(missing)}"
        )

    # Build the shape using only the validated, expected parameters.
    ordered_args = {p: kwargs[p] for p in expected_params}
    return cls(**ordered_args)
