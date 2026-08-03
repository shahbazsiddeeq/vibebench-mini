# src/solution.py

def count_occurrences(arr, target):
    def find_first(arr, target):
        left, right = 0, len(arr) - 1
        first_index = -1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            elif arr[mid] > target:
                right = mid - 1
            else:
                first_index = mid
                right = mid - 1  # continue searching in the left half
        
        return first_index

    def find_last(arr, target):
        left, right = 0, len(arr) - 1
        last_index = -1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < target:
                left = mid + 1
            elif arr[mid] > target:
                right = mid - 1
            else:
                last_index = mid
                left = mid + 1  # continue searching in the right half
        
        return last_index

    first = find_first(arr, target)
    if first == -1:
        return 0  # target not found

    last = find_last(arr, target)
    return last - first + 1
