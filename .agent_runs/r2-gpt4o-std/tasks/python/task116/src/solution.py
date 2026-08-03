from itertools import chain, combinations

def power_set(elements):
    # Remove duplicates by converting to a set
    unique_elements = set(elements)
    
    # Generate all subsets
    all_subsets = chain.from_iterable(combinations(unique_elements, r) for r in range(len(unique_elements) + 1))
    
    # Convert each subset to a frozenset
    frozenset_subsets = [frozenset(subset) for subset in all_subsets]
    
    # Sort by size and then lexicographically by string representation
    frozenset_subsets.sort(key=lambda s: (len(s), sorted(map(str, s))))
    
    return frozenset_subsets
