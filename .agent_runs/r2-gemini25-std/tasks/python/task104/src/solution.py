class Sorter:
    def __init__(self, strategy):
        if not callable(strategy):
            raise TypeError("Strategy must be a callable function.")
        self._strategy = strategy

    def sort(self, data):
        # Ensure the input list is not mutated
        return self._strategy(list(data))

    def set_strategy(self, strategy):
        if not callable(strategy):
            raise TypeError("Strategy must be a callable function.")
        self._strategy = strategy


def bubble_sort(lst):
    n = len(lst)
    # Create a copy to avoid mutating the original list
    arr = list(lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(lst):
    n = len(lst)
    # Create a copy to avoid mutating the original list
    arr = list(lst)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
