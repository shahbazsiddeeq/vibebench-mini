"""Quicksort implementation using only the Python standard library."""


def quicksort(lst):
    """Return a new list containing the elements of *lst* in sorted order.

    The input must be a list and is never modified.
    """
    if not isinstance(lst, list):
        raise TypeError("quicksort expects a list")

    result = list(lst)
    if len(result) < 2:
        return result

    partitions = [(0, len(result) - 1)]

    while partitions:
        low, high = partitions.pop()
        if low >= high:
            continue

        pivot = result[low + (high - low) // 2]
        less = low
        current = low
        greater = high

        # Three-way partition: values below, equal to, and above the pivot.
        while current <= greater:
            if result[current] < pivot:
                result[less], result[current] = result[current], result[less]
                less += 1
                current += 1
            elif pivot < result[current]:
                result[current], result[greater] = (
                    result[greater],
                    result[current],
                )
                greater -= 1
            else:
                current += 1

        if low < less - 1:
            partitions.append((low, less - 1))
        if greater + 1 < high:
            partitions.append((greater + 1, high))

    return result
