"""
Strategy Pattern (Sorter) implementation.

This module provides a Sorter class that uses different sorting strategies,
along with two concrete sorting strategy functions: bubble_sort and insertion_sort.
"""

from typing import Callable, List, Any


def bubble_sort(lst: List[Any]) -> List[Any]:
    """
    Bubble sort strategy function.
    
    Sorts a list using the bubble sort algorithm without mutating the input.
    
    Args:
        lst: A list to be sorted.
        
    Returns:
        A new sorted list.
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Create a copy to avoid mutating the input
    arr = lst.copy()
    n = len(arr)
    
    # Bubble sort algorithm
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    
    return arr


def insertion_sort(lst: List[Any]) -> List[Any]:
    """
    Insertion sort strategy function.
    
    Sorts a list using the insertion sort algorithm without mutating the input.
    
    Args:
        lst: A list to be sorted.
        
    Returns:
        A new sorted list.
    """
    if not isinstance(lst, list):
        raise TypeError("Input must be a list")
    
    # Create a copy to avoid mutating the input
    arr = lst.copy()
    
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
    A class that holds and applies a sorting strategy.
    
    The strategy is a callable that takes a list and returns a new sorted list.
    """
    
    def __init__(self, strategy: Callable[[List[Any]], List[Any]]) -> None:
        """
        Initialize the Sorter with a sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list.
            
        Raises:
            TypeError: If strategy is not callable.
        """
        if not callable(strategy):
            raise TypeError("Strategy must be callable")
        self._strategy = strategy
    
    def sort(self, data: List[Any]) -> List[Any]:
        """
        Sort the data using the current strategy.
        
        Args:
            data: A list to be sorted.
            
        Returns:
            A new sorted list without mutating the input.
            
        Raises:
            TypeError: If data is not a list.
        """
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        
        return self._strategy(data)
    
    def set_strategy(self, strategy: Callable[[List[Any]], List[Any]]) -> None:
        """
        Replace the current sorting strategy.
        
        Args:
            strategy: A callable that takes a list and returns a sorted list.
            
        Raises:
            TypeError: If strategy is not callable.
        """
        if not callable(strategy):
            raise TypeError("Strategy must be callable")
        self._strategy = strategy
