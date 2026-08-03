from itertools import permutations as it_permutations

def permutations(lst):
    if not isinstance(lst, list):
        raise TypeError("Input must be a list.")
    
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8.")
    
    # Generate permutations using itertools
    perm = list(it_permutations(lst))
    
    # Sort permutations in ascending order
    perm.sort()
    
    return perm
