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
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("Inputs 'a' and 'b' must be lists.")
    if not all(isinstance(x, (int, float)) for x in a) or not all(isinstance(x, (int, float)) for x in b):
        raise TypeError("All elements in vectors 'a' and 'b' must be numbers.")

    n = len(a)
    if n == 0:
        raise ValueError("Vectors cannot be empty.")
    if n != len(b):
        raise ValueError("Vectors must have the same length.")

    dot_product = 0.0
    norm_a_sq = 0.0
    norm_b_sq = 0.0

    for i in range(n):
        dot_product += a[i] * b[i]
        norm_a_sq += a[i] * a[i]
        norm_b_sq += b[i] * b[i]

    norm_a = math.sqrt(norm_a_sq)
    norm_b = math.sqrt(norm_b_sq)

    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Cannot compute cosine similarity for a zero vector (zero magnitude).")

    similarity = dot_product / (norm_a * norm_b)

    return round(similarity, 6)
