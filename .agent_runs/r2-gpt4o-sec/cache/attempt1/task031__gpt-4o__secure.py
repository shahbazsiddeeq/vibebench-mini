# src/solution.py

from collections.abc import Iterable

def flatten(nested):
    if not isinstance(nested, Iterable) or isinstance(nested, (str, bytes)):
        raise TypeError("Input must be an iterable of iterables, excluding strings and bytes.")
    
    def _flatten_generator(nested_list):
        for item in nested_list:
            if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                yield from _flatten_generator(item)
            else:
                yield item

    return list(_flatten_generator(nested))
