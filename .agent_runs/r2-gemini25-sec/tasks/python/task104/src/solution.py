import collections.abc

class Sorter:
    """
    Sorter(strategy) holds a sorting strategy, where strategy is a callable that
    takes a list and returns a new sorted list.
    """
    def __init__(self, strategy: collections.abc.Callable[[list], list]):
        """
        Initializes the Sorter with a given strategy.

        Args:
            strategy: A callable that takes a list and returns a new sorted list.
                      Must be a callable.
        Raises:
            TypeError: If the provided strategy is not a callable.
        """
        if not isinstance(strategy, collections.abc.Callable):
            raise TypeError("Strategy must be a callable.")
        self._strategy = strategy

    def sort(self, data: list) -> list:
        """
        Sorts the data using the current strategy WITHOUT mutating the input list.

        Args:
            data: The list to be sorted. Must be a list.
        Returns:
            A new list sorted according to the current strategy.
        Raises:
            TypeError: If the provided data is not a list.
            Exception: If the strategy callable raises an exception during sorting.
        """
        if not isinstance(data, list):
            raise TypeError("Data to be sorted must be a list.")
        
        # The strategy is expected to return a new list, so we don't need to copy here.
        # However, we pass a copy to ensure the strategy itself cannot mutate the original
        # if it were to incorrectly modify its input argument.
        try:
            return self._strategy(list(data))
        except Exception as e:
            # Catching a broad exception here to prevent internal strategy errors
            # from exposing implementation details. Re-raise as a generic error.
            raise RuntimeError(f"Sorting strategy failed: {e}") from e

    def set_strategy(self, strategy: collections.abc.Callable[[list], list]):
        """
        Replaces the current sorting strategy.

        Args:
            strategy: A callable that takes a list and returns a new sorted list.
                      Must be a callable.
        Raises:
            TypeError: If the provided strategy is not a callable.
        """
        if not isinstance(strategy, collections.abc.Callable):
            raise TypeError("Strategy must be a callable.")
        self._strategy = strategy

def bubble_sort(lst: list) -> list:
    """
    Sorts a list using the bubble sort algorithm.

    Args:
        lst: The list to be sorted. Elements must be comparable.
    Returns:
        A new list containing the sorted elements.
    Raises:
        TypeError: If the input is not a list or contains non-comparable elements.
    """
    if not isinstance(lst, list):
        raise TypeError("Input for bubble_sort must be a list.")

    n = len(lst)
    # Create a copy to ensure the original list is not mutated
    arr = list(lst)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            try:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            except TypeError:
                raise TypeError("Elements in the list must be comparable for bubble_sort.")
        if not swapped:
            break
    return arr

def insertion_sort(lst: list) -> list:
    """
    Sorts a list using the insertion sort algorithm.

    Args:
        lst: The list to be sorted. Elements must be comparable.
    Returns:
        A new list containing the sorted elements.
    Raises:
        TypeError: If the input is not a list or contains non-comparable elements.
    """
    if not isinstance(lst, list):
        raise TypeError("Input for insertion_sort must be a list.")

    # Create a copy to ensure the original list is not mutated
    arr = list(lst)
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        try:
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        except TypeError:
            raise TypeError("Elements in the list must be comparable for insertion_sort.")
    return arr
