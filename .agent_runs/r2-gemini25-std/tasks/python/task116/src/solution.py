def power_set(elements):
    """
    Generates the power set of the input list as a list of frozensets.
    Each distinct subset appears exactly once.
    The returned list is sorted first by subset size (ascending), then
    lexicographically by the ascending-sorted list of the string representations
    of the subset's elements.
    """
    unique_elements = sorted(list(set(elements)))
    n = len(unique_elements)
    subsets = []

    for i in range(1 << n):
        current_subset = []
        for j in range(n):
            if (i >> j) & 1:
                current_subset.append(unique_elements[j])
        subsets.append(frozenset(current_subset))

    def sort_key(subset):
        # Sort by size first
        # Then by lexicographical order of string representations of sorted elements
        return (len(subset), tuple(sorted(str(x) for x in subset)))

    subsets.sort(key=sort_key)
    return subsets
