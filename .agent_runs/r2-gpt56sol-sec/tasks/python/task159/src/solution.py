"""Cosine similarity for numeric vectors."""

import math
from numbers import Real
from typing import Iterable


def _validate_vector(vector: Iterable[Real], name: str) -> tuple[float, ...]:
    if isinstance(vector, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a numeric vector")

    try:
        values = tuple(vector)
    except TypeError:
        raise TypeError(f"{name} must be an iterable numeric vector") from None

    converted: list[float] = []
    for value in values:
        if not isinstance(value, Real):
            raise TypeError(f"{name} must contain only real numbers")
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            raise ValueError(f"{name} contains an unsupported numeric value") from None
        if not math.isfinite(number):
            raise ValueError(f"{name} must contain only finite numbers")
        converted.append(number)

    return tuple(converted)


def cosine_similarity(a: Iterable[Real], b: Iterable[Real]) -> float:
    """Return the cosine similarity of two equal-length numeric vectors."""
    vector_a = _validate_vector(a, "a")
    vector_b = _validate_vector(b, "b")

    if len(vector_a) != len(vector_b):
        raise ValueError("vectors must have equal lengths")
    if not vector_a:
        raise ValueError("vectors must not be empty")

    dot_product = sum(x * y for x, y in zip(vector_a, vector_b))
    magnitude_a_squared = sum(x * x for x in vector_a)
    magnitude_b_squared = sum(y * y for y in vector_b)

    if magnitude_a_squared == 0.0 or magnitude_b_squared == 0.0:
        raise ValueError("vectors must have nonzero magnitude")

    magnitude_a = math.sqrt(magnitude_a_squared)
    magnitude_b = math.sqrt(magnitude_b_squared)
    similarity = dot_product / (magnitude_a * magnitude_b)

    if not math.isfinite(similarity):
        raise ValueError("cosine similarity could not be computed")

    return float(round(similarity, 6))
