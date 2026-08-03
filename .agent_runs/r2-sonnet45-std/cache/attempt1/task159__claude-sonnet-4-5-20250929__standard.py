import math


def cosine_similarity(a, b):
    """
    Compute the cosine similarity between two vectors.
    
    Args:
        a: First numeric vector
        b: Second numeric vector
    
    Returns:
        float: Cosine similarity rounded to 6 decimal places
    
    Raises:
        ValueError: If vectors have different lengths, are empty, or have zero magnitude
    """
    # Check if vectors are empty
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Vectors cannot be empty")
    
    # Check if vectors have the same length
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    
    # Compute dot product
    dot_product = sum(x * y for x, y in zip(a, b))
    
    # Compute norms (Euclidean/L2 length)
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    
    # Check for zero magnitude vectors
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors cannot have zero magnitude")
    
    # Compute cosine similarity
    similarity = dot_product / (norm_a * norm_b)
    
    # Round to 6 decimal places
    return round(similarity, 6)
