from itertools import permutations as iter_permutations


def permutations(lst):
    """
    Returns every ordering of lst as a list of tuples, sorted in ascending order.
    
    Args:
        lst: A list to permute
        
    Returns:
        A sorted list of tuples containing all permutations
        
    Raises:
        ValueError: if len(lst) > 8
    """
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8")
    
    # Generate all permutations and convert to sorted list of tuples
    result = list(iter_permutations(lst))
    result.sort()
    
    return result
