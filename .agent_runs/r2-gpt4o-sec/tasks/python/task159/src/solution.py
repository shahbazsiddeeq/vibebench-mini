import math
from typing import List

def cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must be of the same length.")
    if len(a) == 0:
        raise ValueError("Vectors must not be empty.")
    
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vectors must not have zero magnitude.")
    
    cosine_sim = dot_product / (norm_a * norm_b)
    return round(cosine_sim, 6)
