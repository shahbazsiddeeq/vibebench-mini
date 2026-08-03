import math

def permutations(lst):
    """
    Returns every ordering of lst as a list of tuples, sorted in ascending order.
    Permutations are taken by position, not by value, so duplicate elements
    produce duplicate tuples (e.g. permutations([1,1]) -> [(1,1),(1,1)]).
    An empty list returns [()]. Raises ValueError if len(lst) > 8.

    Args:
        lst: The input list.

    Returns:
        A list of tuples representing all permutations, sorted in ascending order.

    Raises:
        ValueError: If len(lst) > 8.
    """
    n = len(lst)
    if n > 8:
        raise ValueError("Input list length cannot exceed 8.")

    if n == 0:
        return [()]

    # Use a list of indices to represent the elements, allowing for positional permutations
    # even with duplicate values.
    indices = list(range(n))
    result = []

    # Recursive helper function to generate permutations
    def generate_permutations(current_permutation_indices, remaining_indices):
        if not remaining_indices:
            # Construct the tuple using the original list elements based on the permuted indices
            result.append(tuple(lst[i] for i in current_permutation_indices))
            return

        for i in range(len(remaining_indices)):
            next_index_to_add = remaining_indices[i]
            new_current_permutation_indices = current_permutation_indices + [next_index_to_add]
            new_remaining_indices = remaining_indices[:i] + remaining_indices[i+1:]
            generate_permutations(new_current_permutation_indices, new_remaining_indices)

    generate_permutations([], indices)

    # Sort the results as required
    result.sort()
    return result
