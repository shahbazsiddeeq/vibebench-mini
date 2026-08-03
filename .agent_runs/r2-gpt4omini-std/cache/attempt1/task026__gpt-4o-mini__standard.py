from itertools import permutations as it_permutations

def permutations(lst):
    if len(lst) > 8:
        raise ValueError("Length of the list must not exceed 8.")
    
    # Generate all permutations using itertools
    perm = list(it_permutations(lst))
    
    # Sort the permutations and convert to list of tuples
    return sorted(perm)
