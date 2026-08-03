"""
src/solution.py

Outlier detection using population z-scores.

Security considerations:
- Input is validated strictly (type and length checks) before processing.
- No use of eval/exec or dynamic code execution.
- No external I/O; the function is pure and side-effect free.
- Errors are raised with generic, non-sensitive messages (no internal
  state, stack traces, or environment details are exposed).
- Uses only the Python standard library.
"""

from numbers import Real
from typing import List, Sequence, Union

Number = Union[int, float]


def find_outliers(data: Sequence[Number], z_threshold: Number = 2.5) -> List[Number]:
    """
    Return the list of values in `data` whose absolute population z-score
    is strictly greater than `z_threshold`, preserving original order.

    The z-score for a value x is computed as:
        z = (x - mean) / population_std

    where population_std = sqrt(mean((x_i - mean)^2)) (divides by N, not N-1).

    Args:
        data: A sequence of numeric values (at least 2 elements required).
        z_threshold: The z-score threshold (must be a non-negative real number).

    Returns:
        A list of the original values considered outliers, in original order.
        Returns an empty list if the population standard deviation is 0.

    Raises:
        ValueError: If `data` is not a valid sequence of at least 2 numbers,
                    or if `z_threshold` is not a valid non-negative number.
        TypeError: If elements of `data` are not real numbers.
    """
    # Validate data is a proper sequence (not a string, not a mapping, etc.)
    if data is None or isinstance(data, (str, bytes, bytearray, dict)):
        raise ValueError("data must be a sequence of numbers")

    try:
        values = list(data)
    except TypeError:
        raise ValueError("data must be an iterable sequence of numbers")

    if len(values) < 2:
        raise ValueError("data must contain at least 2 elements")

    # Validate all elements are real numbers (reject bool explicitly? bool is
    # a subclass of int, but numerically valid, so we allow it).
    for v in values:
        if not isinstance(v, Real):
            raise TypeError("all elements of data must be numeric")

    # Validate z_threshold
    if not isinstance(z_threshold, Real):
        raise ValueError("z_threshold must be a numeric value")
    if isinstance(z_threshold, bool):
        raise ValueError("z_threshold must be a numeric value, not bool")
    if z_threshold < 0:
        raise ValueError("z_threshold must be non-negative")

    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std = variance ** 0.5

    if std == 0:
        return []

    outliers = []
    for x in values:
        z = (x - mean) / std
        if abs(z) > z_threshold:
            outliers.append(x)

    return outliers
