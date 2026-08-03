from collections import Counter


def unique_char_count(s):
    counts = Counter(s)
    result = {}
    for ch in s:
        if counts[ch] == 1:
            result[ch] = 1
    return result
