# src/solution.py

def count_occurrences(arr, target):
    def find_first(arr, target):
        low, high = 0, len(arr) - 1
        first_occurrence = -1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                first_occurrence = mid
                high = mid - 1
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return first_occurrence

    def find_last(arr, target):
        low, high = 0, len(arr) - 1
        last_occurrence = -1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                last_occurrence = mid
                low = mid + 1
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return last_occurrence

    first = find_first(arr, target)
    if first == -1:
        return 0
    last = find_last(arr, target)
    return last - first + 1
