"""
Cosine similarity utility module.

Provides a single function, `cosine_similarity`, which computes the cosine
similarity between two equal-length numeric vectors in a safe, well-validated
manner.
"""

import math
from numbers import Real
from typing import Sequence, Union

Number = Union[int, float]


def _validate_vector(vec: Sequence[Number], name: str) -> None:
    """
    Validate that `vec` is a non-empty sequence of real numbers.

    Raises:
        ValueError: if the vector is not a valid sequence, is empty, or
            contains non-numeric elements.
    """
    if not isinstance(vec, (list, tuple)):
        raise ValueError(f"{name} must be a list or tuple of numbers.")

    if len(vec) == 0:
        raise ValueError(f"{name} must not be empty.")

    for item in vec:
        # Explicitly exclude bool (subclass of int) is not necessary here,
        # since bool is a valid numeric type for this purpose, but we still
        # guard against non-numeric, non-finite, or unsafe values.
        if not isinstance(item, Real):
            raise ValueError(f"{name} must contain only numeric values.")
        if isinstance(item, float) and (math.isnan(item) or math.isinf(item)):
            raise ValueError(f"{name} must contain only finite numbers.")


def cosine_similarity(a: Sequence[Number], b: Sequence[Number]) -> float:
    """
    Compute the cosine similarity between two equal-length numeric vectors.

    Cosine similarity is defined as:
        dot(a, b) / (norm(a) * norm(b))

    where dot(a, b) is the sum of elementwise products and norm(x) is the
    Euclidean (L2) length sqrt(sum(x_i ** 2)).

    Args:
        a: A non-empty sequence of numbers.
        b: A non-empty sequence of numbers, same length as `a`.

    Returns:
        The cosine similarity as a float, rounded to 6 decimal places.

    Raises:
        ValueError: if the vectors have different lengths, either vector is
            empty, either vector contains non-numeric/non-finite values, or
            either vector has zero magnitude (all-zero vector).
    """
    _validate_vector(a, "a")
    _validate_vector(b, "b")

    if len(a) != len(b):
        raise ValueError("Vectors must have the same length.")

    dot_product = 0.0
    norm_a_sq = 0.0
    norm_b_sq = 0.0

    for x, y in zip(a, b):
        dot_product += float(x) * float(y)
        norm_a_sq += float(x) * float(x)
        norm_b_sq += float(y) * float(y)

    norm_a = math.sqrt(norm_a_sq)
    norm_b = math.sqrt(norm_b_sq)

    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Cosine similarity is undefined for zero-magnitude vectors.")

    similarity = dot_product / (norm_a * norm_b)

    return round(float(similarity), 6)
