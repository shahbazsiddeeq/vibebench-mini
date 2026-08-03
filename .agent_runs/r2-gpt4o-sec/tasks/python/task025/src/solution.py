# src/solution.py

def rotate(lst, k):
    if not isinstance(lst, list):
        raise TypeError("The first argument must be a list.")
    if not isinstance(k, int):
        raise TypeError("The second argument must be an integer.")
    
    n = len(lst)
    if n == 0:
        return []
    
    # Normalize k to be within the bounds of the list length
    k = k % n
    
    # Perform the rotation
    return lst[-k:] + lst[:-k]
