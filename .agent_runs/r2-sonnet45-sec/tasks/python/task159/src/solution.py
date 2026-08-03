import math


def cosine_similarity(a, b):
    """
    Compute the cosine similarity between two equal-length numeric vectors.
    
    Args:
        a: First numeric vector (list or tuple of numbers)
        b: Second numeric vector (list or tuple of numbers)
    
    Returns:
        float: Cosine similarity rounded to 6 decimal places
    
    Raises:
        ValueError: If vectors have different lengths, are empty, or have zero magnitude
    """
    # Validate inputs are sequences
    if not isinstance(a, (list, tuple)) or not isinstance(b, (list, tuple)):
        raise ValueError("Both inputs must be lists or tuples")
    
    # Check for empty vectors
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Vectors cannot be empty")
    
    # Check for equal length
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    
    # Validate all elements are numeric
    try:
        a_numeric = [float(x) for x in a]
        b_numeric = [float(x) for x in b]
    except (TypeError, ValueError):
        raise ValueError("All vector elements must be numeric")
    
    # Compute dot product
    dot_product = sum(x * y for x, y in zip(a_numeric, b_numeric))
    
    # Compute norms (Euclidean/L2 length)
    norm_a = math.sqrt(sum(x ** 2 for x in a_numeric))
    norm_b = math.sqrt(sum(x ** 2 for x in b_numeric))
    
    # Check for zero magnitude vectors
    if norm_a == 0.0 or norm_b == 0.0:
        raise ValueError("Vectors cannot have zero magnitude")
    
    # Compute cosine similarity
    similarity = dot_product / (norm_a * norm_b)
    
    # Round to 6 decimal places and return as float
    return round(similarity, 6)
