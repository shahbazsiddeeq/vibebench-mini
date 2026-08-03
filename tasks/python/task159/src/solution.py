import math


def cosine_similarity(a, b):
    """Return cosine similarity dot(a,b)/(||a||*||b||) rounded to 6 decimals.

    Raises ValueError on length mismatch, empty vectors, or a zero-magnitude
    vector.
    """
    if len(a) != len(b):
        raise ValueError("vectors must have equal length")
    if not a or not b:
        raise ValueError("vectors must be non-empty")

    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y

    if norm_a == 0 or norm_b == 0:
        raise ValueError("vectors must have non-zero magnitude")

    return round(dot / (math.sqrt(norm_a) * math.sqrt(norm_b)), 6)
