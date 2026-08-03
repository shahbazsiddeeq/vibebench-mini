from itertools import combinations


def power_set(elements):
    """
    Returns the power set of the input list as a list of frozensets.
    
    Each distinct subset appears exactly once (duplicate elements in the input
    are treated as a single value).
    
    The returned list is sorted first by subset size (ascending), then
    lexicographically by the ascending-sorted list of the string representations
    of the subset's elements.
    
    Args:
        elements: A list of elements
        
    Returns:
        A list of frozensets representing the power set, sorted by size then lexicographically
    """
    # Remove duplicates by converting to set, but keep track of unique elements
    unique_elements = list(set(elements))
    
    # Generate all subsets
    subsets = []
    for r in range(len(unique_elements) + 1):
        for combo in combinations(unique_elements, r):
            subsets.append(frozenset(combo))
    
    # Sort by size first, then lexicographically by string representation
    def sort_key(fs):
        # First sort by size
        size = len(fs)
        # Then by lexicographic order of string representations of sorted elements
        sorted_elements = sorted(fs, key=str)
        string_repr = tuple(str(elem) for elem in sorted_elements)
        return (size, string_repr)
    
    subsets.sort(key=sort_key)
    
    return subsets
