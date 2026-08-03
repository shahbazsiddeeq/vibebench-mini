# src/solution.py

from typing import Callable, Any
import functools

def pipeline(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def composed_function(x: Any) -> Any:
        result = x
        for fn in fns:
            if not callable(fn):
                raise ValueError("All elements in the pipeline must be callable")
            result = fn(result)
        return result
    
    return composed_function
