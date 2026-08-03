from itertools import chain, combinations

def power_set(elements):
    # Remove duplicates by converting to a set and back to a sorted list
    unique_elements = sorted(set(elements))
    
    # Generate all combinations of the unique elements
    all_subsets = chain.from_iterable(combinations(unique_elements, r) for r in range(len(unique_elements) + 1))
    
    # Convert combinations to frozensets
    power_set_result = [frozenset(subset) for subset in all_subsets]
    
    # Sort the result first by size and then lexicographically
    power_set_result.sort(key=lambda x: (len(x), sorted(x)))
    
    return power_set_result
