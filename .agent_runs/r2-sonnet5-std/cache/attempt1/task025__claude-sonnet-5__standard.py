def rotate(lst, k):
    if not lst:
        return []
    n = len(lst)
    k = k % n
    return lst[-k:] + lst[:-k] if k else list(lst)
