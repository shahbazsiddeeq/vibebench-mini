# src/solution.py

import math

def cosine_similarity(a, b):
    # Validate input types
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Both inputs must be lists.")
    
    # Validate lengths
    if len(a) != len(b):
        raise ValueError("Vectors must be of the same length.")
    
    # Validate non-empty vectors
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Vectors must not be empty.")
    
    # Calculate dot product and norms
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(y ** 2 for y in b))
    
    # Validate non-zero magnitude
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be zero vectors.")
    
    # Calculate cosine similarity
    similarity = dot_product / (norm_a * norm_b)
    
    # Return rounded result
    return round(similarity, 6)
