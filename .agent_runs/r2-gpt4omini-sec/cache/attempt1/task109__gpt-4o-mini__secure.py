# src/solution.py

from typing import Callable, Any, Tuple

def pipeline(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Returns a function that applies the given functions left-to-right to its input.
    
    :param fns: A variable number of functions to be composed.
    :return: A function that takes an input and applies the composed functions.
    """
    # Validate that all provided arguments are callable
    for fn in fns:
        if not callable(fn):
            raise TypeError("All arguments must be callable")

    def composed_function(input_value: Any) -> Any:
        result = input_value
        for fn in fns:
            result = fn(result)
        return result

    return composed_function
