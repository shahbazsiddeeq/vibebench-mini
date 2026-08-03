"""
src/solution.py

Provides `weighted_average(values, weights)`, a secure and well-validated
implementation of the weighted arithmetic mean.
"""

from numbers import Real
from typing import List, Sequence, Union

Number = Union[int, float]


def weighted_average(values: Sequence[Number], weights: Sequence[Number]) -> float:
    """
    Compute the weighted arithmetic mean of `values` using `weights`.

    weighted_average = sum(v_i * w_i) / sum(w_i)

    Args:
        values: A sequence of numbers (ints or floats).
        weights: A sequence of numbers (ints or floats), same length as values.

    Returns:
        The weighted average as a float, rounded to 6 decimal places.

    Raises:
        ValueError: If values or weights is empty, if their lengths differ,
                    if any element is not a real number (and not a bool),
                    or if sum(weights) == 0.
    """
    # Validate that inputs are actual sequences (not strings, not generators)
    if isinstance(values, (str, bytes)) or isinstance(weights, (str, bytes)):
        raise ValueError("values and weights must be sequences of numbers, not strings/bytes")

    try:
        values_list: List[Number] = list(values)
        weights_list: List[Number] = list(weights)
    except TypeError as exc:
        raise ValueError("values and weights must be iterable sequences of numbers") from exc

    if len(values_list) == 0 or len(weights_list) == 0:
        raise ValueError("values and weights must be non-empty")

    if len(values_list) != len(weights_list):
        raise ValueError("values and weights must have the same length")

    def _validate_number(x: object, name: str) -> Number:
        # Reject booleans explicitly even though bool is a subclass of int,
        # to avoid silent misuse (True/False are not meaningful weights/values here).
        if isinstance(x, bool):
            raise ValueError(f"{name} must contain only numeric values, not booleans")
        if not isinstance(x, Real):
            raise ValueError(f"{name} must contain only numeric values")
        return x

    validated_values = [_validate_number(v, "values") for v in values_list]
    validated_weights = [_validate_number(w, "weights") for w in weights_list]

    total_weight = sum(validated_weights)

    if total_weight == 0:
        raise ValueError("sum of weights must not be zero")

    weighted_sum = sum(v * w for v, w in zip(validated_values, validated_weights))

    result = weighted_sum / total_weight

    return round(float(result), 6)
