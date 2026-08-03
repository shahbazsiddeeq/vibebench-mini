import math

def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Calculates the cosine similarity between two equal-length numeric vectors.

    Args:
        a: The first numeric vector.
        b: The second numeric vector.

    Returns:
        The cosine similarity as a float, rounded to 6 decimal places.

    Raises:
        ValueError: If the vectors have different lengths, if either vector is empty,
                    or if either vector has zero magnitude.
    """
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length.")
    if not a:  # Checks if vector a is empty (and by extension, b as well)
        raise ValueError("Vectors cannot be empty.")

    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a_sq = sum(x * x for x in a)
    norm_b_sq = sum(y * y for y in b)

    if norm_a_sq == 0 or norm_b_sq == 0:
        raise ValueError("Vectors with zero magnitude are not allowed.")

    norm_a = math.sqrt(norm_a_sq)
    norm_b = math.sqrt(norm_b_sq)

    similarity = dot_product / (norm_a * norm_b)

    return round(similarity, 6)
