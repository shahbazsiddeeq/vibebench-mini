from itertools import permutations as _itertools_permutations


def permutations(lst):
    """Return all positional permutations of *lst* as sorted tuples."""
    if len(lst) > 8:
        raise ValueError("permutations supports at most 8 elements")
    return sorted(_itertools_permutations(lst))
