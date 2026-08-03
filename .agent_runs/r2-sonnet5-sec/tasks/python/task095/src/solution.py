"""
src/solution.py

A secure, self-contained implementation of a percentile calculator.

The public function `percentile(data, p)` computes the p-th percentile of a
sequence of numeric values using linear interpolation (the same method used
by numpy's default 'linear' interpolation and many statistics packages).

Security considerations:
- No use of eval/exec or dynamic code execution.
- No external I/O; the module performs no network or file access.
- All inputs are validated defensively; malformed or malicious input results
  in a clear ValueError/TypeError rather than silent misbehavior or crashes
  that could leak internal state.
- Randomness is not required for this task, but if any random values were
  needed, the `secrets` module would be used instead of `random`.
"""

from numbers import Real
from typing import Sequence, List


def _validate_data(data: Sequence) -> List[float]:
    """
    Validate that `data` is a non-empty sequence of real numbers and
    return a sorted list of floats.

    Raises:
        ValueError: if data is empty or contains non-numeric values.
        TypeError: if data is not an iterable sequence at all.
    """
    if data is None:
        raise ValueError("data must not be None")

    try:
        items = list(data)
    except TypeError as exc:
        raise TypeError("data must be an iterable sequence of numbers") from exc

    if len(items) == 0:
        raise ValueError("data must not be empty")

    validated: List[float] = []
    for item in items:
        # Explicitly reject booleans being treated oddly, but bool is a
        # subclass of int so it's still numeric; that's fine for percentile
        # computation (True == 1, False == 0). We just ensure it's Real.
        if not isinstance(item, Real):
            raise ValueError("data must contain only numeric values")
        validated.append(float(item))

    validated.sort()
    return validated


def _validate_percentile(p) -> float:
    """
    Validate that p is a real number in the inclusive range [0, 100].

    Raises:
        ValueError: if p is not within [0, 100].
        TypeError: if p is not a real number.
    """
    if not isinstance(p, Real):
        raise TypeError("p must be a numeric value")

    p_val = float(p)

    if p_val < 0 or p_val > 100:
        raise ValueError("p must be between 0 and 100 inclusive")

    return p_val


def percentile(data: Sequence, p) -> float:
    """
    Compute the p-th percentile of `data` using linear interpolation.

    Args:
        data: A non-empty sequence of numeric values.
        p: A number in the range [0, 100] representing the desired
           percentile.

    Returns:
        The p-th percentile as a float.

    Raises:
        ValueError: if data is empty, contains non-numeric values, or if p
                    is outside the range [0, 100].
        TypeError: if data or p are of invalid types.
    """
    sorted_data = _validate_data(data)
    p_val = _validate_percentile(p)

    n = len(sorted_data)

    if n == 1:
        return sorted_data[0]

    # Rank position using linear interpolation between closest ranks.
    rank = (p_val / 100.0) * (n - 1)
    lower_index = int(rank)  # floor, since rank >= 0
    upper_index = min(lower_index + 1, n - 1)
    fraction = rank - lower_index

    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]

    result = lower_value + (upper_value - lower_value) * fraction
    return float(result)
