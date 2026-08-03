def quicksort(lst):
    if len(lst) <= 1:
        return list(lst)
    pivot = lst[len(lst) // 2]
    less = [x for x in lst if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]
    return quicksort(less) + equal + quicksort(greater)
