"""Module providing permutations function."""
import itertools


def permutations(lst):
    """
    Return every ordering of lst as a list of tuples, sorted in ascending order.

    Permutations are taken by position, not by value, so duplicate elements
    produce duplicate tuples.

    Raises ValueError if len(lst) > 8.
    """
    if len(lst) > 8:
        raise ValueError("List length must not exceed 8")

    indices = range(len(lst))
    perms = [tuple(lst[i] for i in perm) for perm in itertools.permutations(indices)]
    return sorted(perms)
