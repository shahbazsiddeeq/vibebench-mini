import math
from typing import Sequence, Union


def cosine_similarity(a: Sequence[Union[int, float]], b: Sequence[Union[int, float]]) -> float:
    """
    Compute the cosine similarity between two equal-length numeric vectors.
    
    Args:
        a: First numeric vector
        b: Second numeric vector
        
    Returns:
        Cosine similarity as a float rounded to 6 decimal places
        
    Raises:
        ValueError: If vectors have different lengths, are empty, or have zero magnitude
    """
    # Validate inputs are sequences
    if not isinstance(a, Sequence) or not isinstance(b, Sequence):
        raise ValueError("Both inputs must be sequences")
    
    # Check lengths match
    if len(a) != len(b):
        raise ValueError("Vectors must have equal length")
    
    # Check vectors are not empty
    if len(a) == 0:
        raise ValueError("Vectors cannot be empty")
    
    # Validate all elements are numeric
    try:
        a_list = [float(x) for x in a]
        b_list = [float(x) for x in b]
    except (TypeError, ValueError):
        raise ValueError("All vector elements must be numeric")
    
    # Compute dot product
    dot_product = sum(x * y for x, y in zip(a_list, b_list))
    
    # Compute norms
    norm_a = math.sqrt(sum(x * x for x in a_list))
    norm_b = math.sqrt(sum(x * x for x in b_list))
    
    # Check for zero magnitude vectors
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors cannot have zero magnitude")
    
    # Compute cosine similarity
    similarity = dot_product / (norm_a * norm_b)
    
    # Round to 6 decimal places
    return round(similarity, 6)
