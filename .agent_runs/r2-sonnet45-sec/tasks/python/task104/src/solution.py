"""
Strategy Pattern implementation for sorting algorithms.
Provides a Sorter class that uses different sorting strategies,
along with bubble_sort and insertion_sort implementations.
"""


def bubble_sort(lst):
    """
    Sorts a list using bubble sort algorithm.
    Returns a new sorted list without mutating the input.
    
    Args:
        lst: A list to sort
        
    Returns:
        A new sorted list
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Create a copy to avoid mutating the original
    result = lst.copy()
    n = len(result)
    
    # Bubble sort algorithm
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        # Optimization: if no swaps occurred, list is sorted
        if not swapped:
            break
    
    return result


def insertion_sort(lst):
    """
    Sorts a list using insertion sort algorithm.
    Returns a new sorted list without mutating the input.
    
    Args:
        lst: A list to sort
        
    Returns:
        A new sorted list
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Create a copy to avoid mutating the original
    result = lst.copy()
    
    # Insertion sort algorithm
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    
    return result


class Sorter:
    """
    A class that uses the Strategy pattern to sort data using different algorithms.
    """
    
    def __init__(self, strategy):
        """
        Initialize the Sorter with a sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list
        """
        if not callable(strategy):
            raise TypeError("Strategy must be callable")
        self._strategy = strategy
    
    def sort(self, data):
        """
        Sort the data using the current strategy.
        
        Args:
            data: A list to sort
            
        Returns:
            A new sorted list (does not mutate input)
        """
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        
        # Call the strategy function with the data
        return self._strategy(data)
    
    def set_strategy(self, strategy):
        """
        Replace the current sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list
        """
        if not callable(strategy):
            raise TypeError("Strategy must be callable")
        self._strategy = strategy
