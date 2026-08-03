# src/solution.py

import math

def cosine_similarity(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must be of the same length.")
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Vectors must not be empty.")
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x ** 2 for x in a))
    norm_b = math.sqrt(sum(y ** 2 for y in b))
    
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not be zero vectors.")
    
    similarity = dot_product / (norm_a * norm_b)
    return round(similarity, 6)
