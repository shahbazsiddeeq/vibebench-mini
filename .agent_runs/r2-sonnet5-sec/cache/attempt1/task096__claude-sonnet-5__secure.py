"""
src/solution.py

Provides a secure, validated implementation of a simple moving average
calculation.

The module intentionally avoids any use of eval/exec, external I/O, or
non-deterministic behavior. All inputs are validated defensively before
computation, and errors are surfaced via well-defined exceptions without
leaking internal state or stack details.
"""

from numbers import Real
from typing import List, Sequence


def moving_average(data: Sequence[Real], window: int) -> List[float]:
    """
    Compute the simple moving average of `data` using the given `window` size.

    Args:
        data: A sequence of numeric values (ints or floats).
        window: The size of the moving average window (positive integer).

    Returns:
        A list of floats representing the moving averages. The length of the
        result is len(data) - window + 1.

    Raises:
        ValueError: If `window` is not a positive integer, if `window` is
            greater than the length of `data`, or if `data` contains
            non-numeric values.
        TypeError: If `data` is not a sequence or `window` is not an integer.
    """
    # Validate `data` type
    if isinstance(data, (str, bytes)) or not isinstance(data, Sequence):
        raise TypeError("data must be a sequence of numbers (e.g., list or tuple)")

    # Validate `window` type strictly (reject bool, float, etc.)
    if isinstance(window, bool) or not isinstance(window, int):
        raise TypeError("window must be an integer")

    # Validate window value
    if window <= 0:
        raise ValueError("window must be a positive integer")

    data_len = len(data)

    if window > data_len:
        raise ValueError("window cannot be greater than the length of data")

    # Validate that all elements are numeric (int/float), reject bool explicitly
    # to avoid silent coercion issues, though bool is technically an int subtype.
    validated_data = []
    for idx, value in enumerate(data):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"data must contain only numeric values (index {idx} is invalid)")
        validated_data.append(float(value))

    # Compute moving averages using a running sum for efficiency and to avoid
    # repeated floating-point summation errors from re-summing full windows.
    result: List[float] = []
    window_sum = sum(validated_data[:window])
    result.append(window_sum / window)

    for i in range(window, data_len):
        window_sum += validated_data[i] - validated_data[i - window]
        result.append(window_sum / window)

    return result
