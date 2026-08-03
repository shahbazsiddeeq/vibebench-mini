"""
src/solution.py

A small, self-contained module implementing ordinary least squares
linear regression for paired numeric data.

Security considerations:
- No use of eval/exec or dynamic code execution.
- No file, network, or subprocess I/O.
- All inputs are strictly validated before use.
- Errors are raised with generic, non-sensitive messages (no internal
  state, tracebacks, or system details are exposed).
- Only the Python standard library is used.
"""

from numbers import Real
from typing import List, Sequence, Tuple


def _validate_numeric_sequence(values: Sequence, name: str) -> List[float]:
    """
    Validate that `values` is a sequence of real numbers (int/float, not bool)
    and return a list of floats.

    Raises:
        ValueError: if `values` is not a valid sequence of real numbers.
    """
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of numbers, not text.")

    try:
        items = list(values)
    except TypeError:
        raise ValueError(f"{name} must be an iterable of numbers.")

    result: List[float] = []
    for item in items:
        # Explicitly reject booleans since bool is a subclass of int.
        if isinstance(item, bool) or not isinstance(item, Real):
            raise ValueError(f"All elements of {name} must be real numbers.")
        result.append(float(item))

    return result


def linear_regression(xs: Sequence, ys: Sequence) -> Tuple[float, float]:
    """
    Fit a simple ordinary least squares line y = slope * x + intercept
    to the paired data in `xs` and `ys`.

    Args:
        xs: sequence of x-values (numeric).
        ys: sequence of y-values (numeric).

    Returns:
        A tuple (slope, intercept), each a float rounded to 6 decimal places.

    Raises:
        ValueError: if xs and ys have different lengths, if there are
            fewer than 2 points, or if all x-values are identical
            (undefined slope for a vertical line).
    """
    x_values = _validate_numeric_sequence(xs, "xs")
    y_values = _validate_numeric_sequence(ys, "ys")

    if len(x_values) != len(y_values):
        raise ValueError("xs and ys must have the same length.")

    n = len(x_values)
    if n < 2:
        raise ValueError("At least two data points are required.")

    mx = sum(x_values) / n
    my = sum(y_values) / n

    numerator = sum((x - mx) * (y - my) for x, y in zip(x_values, y_values))
    denominator = sum((x - mx) ** 2 for x in x_values)

    if denominator == 0:
        raise ValueError("All x values are identical; slope is undefined.")

    slope = numerator / denominator
    intercept = my - slope * mx

    return (round(float(slope), 6), round(float(intercept), 6))
