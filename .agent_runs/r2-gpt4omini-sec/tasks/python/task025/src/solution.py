# src/solution.py

def rotate(lst, k):
    if not isinstance(lst, list):
        raise ValueError("Input must be a list.")
    
    if not all(isinstance(item, (int, float)) for item in lst):
        raise ValueError("All items in the list must be integers or floats.")
    
    if not isinstance(k, int):
        raise ValueError("Rotation count must be an integer.")
    
    n = len(lst)
    if n == 0:
        return []
    
    k = k % n  # Normalize k to avoid unnecessary rotations
    if k < 0:
        k += n  # Convert negative rotations to positive
    
    return lst[-k:] + lst[:-k]
