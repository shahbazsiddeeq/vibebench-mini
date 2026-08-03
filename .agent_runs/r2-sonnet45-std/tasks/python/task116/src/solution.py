def power_set(elements):
    # Remove duplicates by converting to set
    unique_elements = list(set(elements))
    
    # Generate all subsets
    subsets = []
    n = len(unique_elements)
    
    # Use bit manipulation to generate all 2^n subsets
    for i in range(2 ** n):
        subset = frozenset(
            unique_elements[j] for j in range(n) if (i >> j) & 1
        )
        subsets.append(subset)
    
    # Sort by size first, then lexicographically by sorted string representations
    def sort_key(s):
        # First sort by size
        # Then by the sorted list of string representations of elements
        return (len(s), sorted(str(elem) for elem in s))
    
    subsets.sort(key=sort_key)
    
    return subsets
