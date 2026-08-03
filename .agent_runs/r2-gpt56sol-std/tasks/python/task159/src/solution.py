import math
from typing import Sequence


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Return the cosine similarity of two equal-length numeric vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must have equal lengths")
    if not a:
        raise ValueError("Vectors must not be empty")

    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x ** 2 for x in a))
    magnitude_b = math.sqrt(sum(y ** 2 for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cosine similarity is undefined for zero vectors")

    return float(round(dot_product / (magnitude_a * magnitude_b), 6))
