"""Simple moving average implementation."""

from operator import index
from typing import Iterable, List


def moving_average(data: Iterable[float], window: int) -> List[float]:
    """Return the simple moving averages for each consecutive window.

    Raises:
        TypeError: If ``window`` is not an integer or ``data`` is not iterable.
        ValueError: If ``window`` is non-positive or exceeds the data length.
    """
    if isinstance(window, bool):
        raise TypeError("window must be an integer")

    try:
        window_size = index(window)
    except TypeError:
        raise TypeError("window must be an integer") from None

    try:
        values = list(data)
    except TypeError:
        raise TypeError("data must be iterable") from None

    if window_size <= 0 or window_size > len(values):
        raise ValueError("window must be positive and no greater than data length")

    try:
        current_sum = sum(values[:window_size])
        result = [float(current_sum / window_size)]

        for position in range(window_size, len(values)):
            current_sum += values[position] - values[position - window_size]
            result.append(float(current_sum / window_size))
    except (TypeError, ValueError, OverflowError):
        raise TypeError("data must contain compatible numeric values") from None

    return result
