"""
src/solution.py

Descriptive statistics utility.

Provides a single function, `describe`, which computes common descriptive
statistics for a sequence of numeric values.

Security considerations:
- No use of eval/exec or other dynamic code execution.
- No I/O operations.
- Input is strictly validated: only numeric (int/float, excluding bool) values
  are accepted; anything else raises a clear, non-leaking TypeError.
- Uses only the Python standard library.
- Errors raised do not expose internal state or stack details beyond a safe
  message.
"""

from collections import Counter
from statistics import mean as _mean, median as _median
from numbers import Real
from typing import Any, Dict, List, Optional, Sequence


def _validate_data(data: Any) -> List[float]:
    """
    Validate that `data` is a non-empty sequence of real numbers.

    Raises:
        ValueError: if data is empty or not a valid sequence.
        TypeError: if data contains non-numeric or boolean values.
    """
    if data is None:
        raise ValueError("data must not be None")

    if isinstance(data, (str, bytes)):
        raise TypeError("data must be a sequence of numbers, not a string/bytes")

    try:
        items = list(data)
    except TypeError as exc:
        raise TypeError("data must be an iterable of numbers") from exc

    if len(items) == 0:
        raise ValueError("data must not be empty")

    validated: List[float] = []
    for item in items:
        # Explicitly reject booleans even though bool is a subclass of int.
        if isinstance(item, bool):
            raise TypeError("boolean values are not valid numeric data")
        if not isinstance(item, Real):
            raise TypeError("all elements of data must be numeric (int or float)")
        validated.append(item)

    return validated


def _population_std_dev(values: Sequence[float], avg: float) -> float:
    """Compute the population standard deviation (ddof=0)."""
    n = len(values)
    if n == 1:
        return 0.0
    variance = sum((x - avg) ** 2 for x in values) / n
    return variance ** 0.5


def _compute_mode(values: Sequence[float]) -> Optional[float]:
    """
    Compute the mode: the most frequent value.

    - Ties are broken by choosing the smallest value among those tied.
    - If every value is unique (max frequency == 1), returns None.
    """
    counts = Counter(values)
    max_freq = max(counts.values())
    if max_freq == 1:
        return None
    candidates = [val for val, freq in counts.items() if freq == max_freq]
    return min(candidates)


def describe(data: Sequence[Any]) -> Dict[str, Any]:
    """
    Compute descriptive statistics for a sequence of numeric values.

    Args:
        data: A non-empty sequence of int/float values.

    Returns:
        A dict with keys: count, mean, median, mode, std_dev, min, max, range.
        All numeric values except 'count' are rounded to 4 decimal places.

    Raises:
        ValueError: if data is empty.
        TypeError: if data contains non-numeric values.
    """
    values = _validate_data(data)

    count = len(values)
    avg = _mean(values)
    med = _median(values)
    mode_val = _compute_mode(values)
    std_dev = _population_std_dev(values, avg)
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val

    def _round(x: float) -> float:
        return round(x, 4)

    result: Dict[str, Any] = {
        "count": count,
        "mean": _round(avg),
        "median": _round(med),
        "mode": mode_val,
        "std_dev": _round(std_dev),
        "min": min_val,
        "max": max_val,
        "range": range_val,
    }

    return result
