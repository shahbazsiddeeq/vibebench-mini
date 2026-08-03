def bubble_sort(lst):
    """Bubble sort implementation that returns a new sorted list."""
    result = lst.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def insertion_sort(lst):
    """Insertion sort implementation that returns a new sorted list."""
    result = lst.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


class Sorter:
    """A sorter that uses a configurable sorting strategy."""
    
    def __init__(self, strategy):
        """Initialize with a sorting strategy (callable)."""
        self.strategy = strategy
    
    def sort(self, data):
        """Sort data using the current strategy, returning a new list."""
        return self.strategy(data)
    
    def set_strategy(self, strategy):
        """Replace the current sorting strategy."""
        self.strategy = strategy
