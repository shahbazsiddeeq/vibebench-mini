# src/solution.py

def min_max_normalize(values, new_min=0.0, new_max=1.0):
    if not isinstance(values, list):
        raise ValueError("Input must be a list.")
    
    if len(values) == 0:
        raise ValueError("Input list cannot be empty.")
    
    if not all(isinstance(x, (int, float)) for x in values):
        raise ValueError("All elements in the input list must be numbers.")
    
    lo = min(values)
    hi = max(values)
    
    if hi == lo:
        return [round(float(new_min), 6)] * len(values)
    
    normalized_values = [
        round(new_min + (x - lo) / (hi - lo) * (new_max - new_min), 6)
        for x in values
    ]
    
    return normalized_values
