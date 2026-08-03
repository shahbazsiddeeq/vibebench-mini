"""
src/solution.py

A small, security-conscious utility module implementing a function
composition pipeline.

pipeline(*fns) returns a callable that applies the supplied functions
left-to-right to a single input value.

Example:
    double = lambda x: x * 2
    inc = lambda x: x + 1
    pipeline(double, inc)(3) -> 7

Design notes / security considerations:
- No use of eval/exec or dynamic code execution.
- All arguments are validated to be callables before use.
- No I/O or printing is performed.
- Errors raised by user-supplied functions are not swallowed or hidden,
  but we avoid leaking internal implementation details beyond what the
  standard exception mechanism already provides.
"""

from typing import Any, Callable


def pipeline(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Compose an arbitrary number of unary functions into a single function
    that applies them left-to-right.

    Args:
        *fns: Zero or more callables, each accepting exactly one argument
              and returning a value.

    Returns:
        A callable that takes a single argument, applies each function
        in `fns` in order (output of one feeds into the next), and
        returns the final result. If no functions are provided, the
        returned callable is the identity function.

    Raises:
        TypeError: If any of the provided arguments is not callable.
    """
    # Validate inputs up-front so misuse fails fast and predictably,
    # rather than raising a confusing error deep inside composition.
    validated_fns = []
    for index, fn in enumerate(fns):
        if not callable(fn):
            raise TypeError(
                f"Argument at position {index} is not callable: "
                f"expected a function, got {type(fn).__name__}"
            )
        validated_fns.append(fn)

    def composed(value: Any) -> Any:
        result = value
        for fn in validated_fns:
            result = fn(result)
        return result

    return composed
