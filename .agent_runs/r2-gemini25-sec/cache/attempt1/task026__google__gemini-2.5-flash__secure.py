def permutations(lst):
    """
    Returns every ordering of lst as a list of tuples, sorted in ascending order.
    Permutations are taken by position, not by value, so duplicate elements
    produce duplicate tuples (e.g. permutations([1,1]) -> [(1,1),(1,1)]).
    An empty list returns [()]. Raises ValueError if len(lst) > 8.

    Args:
        lst: A list of elements.

    Returns:
        A list of tuples, where each tuple is a permutation of the input list.

    Raises:
        ValueError: If the length of the input list is greater than 8.
        TypeError: If the input is not a list.
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list.")

    n = len(lst)
    if n > 8:
        raise ValueError("Input list length cannot exceed 8.")

    if n == 0:
        return [()]

    # Using Heap's algorithm for generating permutations
    # This algorithm generates permutations in lexicographical order if the initial list is sorted.
    # However, the problem statement requires the *output* list of tuples to be sorted.
    # So, we generate all permutations and then sort them.

    result = []
    indices = list(range(n))
    c = [0] * n

    # Initial permutation
    current_permutation = [lst[i] for i in indices]
    result.append(tuple(current_permutation))

    i = 1
    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                indices[0], indices[i] = indices[i], indices[0]
            else:
                indices[c[i]], indices[i] = indices[i], indices[c[i]]

            current_permutation = [lst[idx] for idx in indices]
            result.append(tuple(current_permutation))

            c[i] += 1
            i = 1
        else:
            c[i] = 0
            i += 1

    # Sort the results as required by the problem description
    result.sort()
    return result
