from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        key = ''.join(sorted(word))
        groups[key].append(word)

    result = []
    for key in groups:
        result.append(sorted(groups[key]))

    result.sort(key=lambda g: g[0])
    return result
