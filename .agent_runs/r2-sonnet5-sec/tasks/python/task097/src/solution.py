"""
Z-Score Normalizer

Provides a single function, z_scores, that computes the population
z-score ((x - mean) / std) for each element in a numeric sequence.

Security considerations:
- All inputs are validated for type and structure before processing.
- No use of eval/exec or other unsafe constructs.
- No external I/O; purely computational.
- Errors are raised with clear, non-sensitive messages (no internal
  state or stack traces leaked).
"""

from numbers import Real
from typing import List, Sequence


def z_scores(data: Sequence[Real]) -> List[float]:
    """
    Compute the population z-score for each element in `data`.

    z = (x - mean) / std, where std is the population standard
    deviation (ddof=0).

    Args:
        data: A sequence of numeric values.

    Returns:
        A list of floats representing the z-score of each input value,
        in the same order as `data`.

    Raises:
        ValueError: If `data` is not a valid sequence of at least two
            numeric values, or if the population standard deviation is
            zero (i.e., all values are identical).
        TypeError: If `data` is not a sequence or contains non-numeric
            values.
    """
    if data is None:
        raise ValueError("data must not be None")

    if isinstance(data, (str, bytes)):
        raise TypeError("data must be a sequence of numbers, not a string/bytes")

    try:
        values = list(data)
    except TypeError as exc:
        raise TypeError("data must be an iterable sequence of numbers") from exc

    n = len(values)
    if n < 2:
        raise ValueError("data must contain at least two elements")

    for item in values:
        if isinstance(item, bool) or not isinstance(item, Real):
            raise TypeError("all elements in data must be real numbers")

    floats = [float(v) for v in values]

    mean = sum(floats) / n
    variance = sum((x - mean) ** 2 for x in floats) / n
    std = variance ** 0.5

    if std == 0:
        raise ValueError("standard deviation is zero; cannot compute z-scores")

    return [(x - mean) / std for x in floats]
