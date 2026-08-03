def bubble_sort(lst):
    """
    Bubble sort strategy that returns a new sorted list without mutating the input.
    """
    # Create a copy to avoid mutating the input
    arr = lst[:]
    n = len(arr)
    
    # Bubble sort algorithm
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def insertion_sort(lst):
    """
    Insertion sort strategy that returns a new sorted list without mutating the input.
    """
    # Create a copy to avoid mutating the input
    arr = lst[:]
    
    # Insertion sort algorithm
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


class Sorter:
    """
    Sorter class that holds a sorting strategy and can sort data using that strategy.
    """
    
    def __init__(self, strategy):
        """
        Initialize the Sorter with a sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list
        """
        self.strategy = strategy
    
    def sort(self, data):
        """
        Sort the data using the current strategy without mutating the input.
        
        Args:
            data: The list to sort
            
        Returns:
            A new sorted list
        """
        return self.strategy(data)
    
    def set_strategy(self, strategy):
        """
        Replace the current sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list
        """
        self.strategy = strategy
