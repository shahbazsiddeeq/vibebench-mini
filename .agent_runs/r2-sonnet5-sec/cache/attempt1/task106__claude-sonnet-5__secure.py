"""
src/solution.py

A small, security-conscious utility module providing a `histogram` function
that bins numeric data into equal-width intervals.

Design notes / security considerations:
- No use of eval/exec or any dynamic code execution.
- No file, network, or subprocess I/O.
- Strict validation of inputs (types, emptiness, numeric-ness) with clear
  ValueError messages that do not leak internal state or stack details.
- Uses only the Python standard library.
- Defensive handling of edge cases (single value, non-finite numbers,
  non-numeric entries) to avoid unexpected exceptions leaking internals.
"""

from numbers import Real
from typing import List, Sequence, Tuple


def _validate_data(data: Sequence) -> List[float]:
    """
    Validate that `data` is a non-empty sequence of finite real numbers.
    Returns a list of floats (converted) for further processing.

    Raises:
        ValueError: if data is empty, not a sequence, or contains
                    non-numeric / non-finite values.
    """
    if data is None:
        raise ValueError("data must not be None")

    # Explicitly reject strings/bytes even though they are sequences,
    # since iterating them would yield characters, not numbers.
    if isinstance(data, (str, bytes)):
        raise ValueError("data must be a sequence of numbers, not a string")

    try:
        items = list(data)
    except TypeError as exc:
        raise ValueError("data must be an iterable of numbers") from exc

    if len(items) == 0:
        raise ValueError("data must not be empty")

    values: List[float] = []
    for item in items:
        if isinstance(item, bool) or not isinstance(item, Real):
            raise ValueError("data must contain only numeric values")
        val = float(item)
        if val != val or val in (float("inf"), float("-inf")):
            raise ValueError("data must contain only finite numeric values")
        values.append(val)

    return values


def _validate_bins(bins: int) -> int:
    """
    Validate that `bins` is a positive integer.

    Raises:
        ValueError: if bins is not an integer or is less than 1.
    """
    if isinstance(bins, bool) or not isinstance(bins, int):
        raise ValueError("bins must be an integer")
    if bins < 1:
        raise ValueError("bins must be >= 1")
    return bins


def histogram(data: Sequence, bins: int) -> List[Tuple[float, float, int]]:
    """
    Compute an equal-width histogram over `data` with `bins` bins.

    Each bin is represented as (bin_start, bin_end, count), where bin
    edges are floats spanning [min(data), max(data)].

    Binning rule:
        - Each bin is half-open [bin_start, bin_end), EXCEPT the final
          bin which is closed [bin_start, bin_end] so that max(data)
          is always counted.
        - A value on an interior edge belongs to the upper bin.

    Special case:
        - If all values in data are equal, a single bin (v, v, len(data))
          is returned regardless of the `bins` argument (as long as it
          is valid, i.e. >= 1).

    Args:
        data: A non-empty sequence of numeric values.
        bins: A positive integer number of bins.

    Returns:
        A list of (bin_start, bin_end, count) tuples.

    Raises:
        ValueError: if bins < 1, data is empty, or data/bins are of
                    invalid type/content.
    """
    values = _validate_data(data)
    bins = _validate_bins(bins)

    lo = min(values)
    hi = max(values)

    if lo == hi:
        return [(float(lo), float(hi), len(values))]

    width = (hi - lo) / bins

    # Precompute bin edges to avoid floating point drift from repeated
    # addition; edges[i] is the start of bin i, edges[bins] == hi.
    edges = [lo + i * width for i in range(bins)]
    edges.append(hi)

    counts = [0] * bins
    for v in values:
        if v == hi:
            # Max value always goes in the last bin (closed on the right).
            counts[bins - 1] += 1
            continue

        # Compute a candidate index via proportional placement, then
        # adjust for floating point edge cases by checking neighbors.
        idx = int((v - lo) / width)

        # Clamp to valid range defensively.
        if idx < 0:
            idx = 0
        elif idx >= bins:
            idx = bins - 1

        # Correct for floating point inaccuracies: ensure edges[idx] <= v < edges[idx+1]
        while idx > 0 and v < edges[idx]:
            idx -= 1
        while idx < bins - 1 and v >= edges[idx + 1]:
            idx += 1

        counts[idx] += 1

    result: List[Tuple[float, float, int]] = []
    for i in range(bins):
        result.append((float(edges[i]), float(edges[i + 1]), counts[i]))

    return result
