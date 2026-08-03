from itertools import combinations


def power_set(elements):
    unique = list(set(elements))
    subsets = []
    for r in range(len(unique) + 1):
        for combo in combinations(unique, r):
            subsets.append(frozenset(combo))

    def sort_key(s):
        return (len(s), sorted(str(x) for x in s))

    subsets.sort(key=sort_key)
    return subsets
