def rotate(lst, k):
    if not lst:
        return []
    
    n = len(lst)
    k = k % n  # Normalize k to be within the bounds of the list length
    return lst[-k:] + lst[:-k]
