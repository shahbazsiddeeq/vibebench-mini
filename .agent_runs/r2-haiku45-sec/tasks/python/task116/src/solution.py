"""Power Set Generator module."""

from itertools import combinations


def power_set(elements):
    """
    Generate the power set of the input list as a list of frozensets.
    
    Each distinct subset appears exactly once. Duplicate elements in the input
    are treated as a single value.
    
    The returned list is sorted first by subset size (ascending), then
    lexicographically by the ascending-sorted list of the string representations
    of the subset's elements.
    
    Args:
        elements: A list of elements (may contain duplicates).
    
    Returns:
        A list of frozensets representing the power set, sorted by size then
        lexicographically by string representations of elements.
    
    Raises:
        TypeError: If elements is not iterable.
    """
    # Validate input
    if not hasattr(elements, '__iter__') or isinstance(elements, (str, bytes)):
        raise TypeError("elements must be an iterable (but not a string or bytes)")
    
    # Convert to list and remove duplicates while preserving uniqueness
    unique_elements = list(set(elements))
    
    # Generate all subsets using combinations
    power_set_list = []
    for r in range(len(unique_elements) + 1):
        for combo in combinations(unique_elements, r):
            power_set_list.append(frozenset(combo))
    
    # Sort by size first, then lexicographically by string representations
    def sort_key(fs):
        # First key: size of the frozenset
        size = len(fs)
        # Second key: sorted list of string representations
        sorted_elements = sorted(str(elem) for elem in fs)
        return (size, sorted_elements)
    
    power_set_list.sort(key=sort_key)
    
    return power_set_list
