import math


def cosine_similarity(a, b):
    if len(a) != len(b) or len(a) == 0:
        raise ValueError("Vectors must be non-empty and of equal length")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must have non-zero magnitude")

    return round(dot / (norm_a * norm_b), 6)
