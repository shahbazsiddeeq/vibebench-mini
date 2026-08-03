"""Two Sum solution."""

from typing import Iterable, Tuple, Any


def two_sum(nums: Iterable[Any], target: Any) -> Tuple[int, int]:
    """Return the required pair of indices whose values sum to *target*.

    The pair with the smallest second index is returned. For that second
    index, the closest preceding matching index is preferred.

    Raises:
        TypeError: If the inputs do not support the required arithmetic or
            hashing operations.
        ValueError: If no matching pair exists.
    """
    if isinstance(nums, (str, bytes, bytearray)) or nums is None:
        raise TypeError("nums must be an iterable of compatible values")

    latest_index = {}
    sentinel = object()

    try:
        iterator = iter(nums)
    except TypeError:
        raise TypeError("nums must be an iterable of compatible values") from None

    try:
        for j, value in enumerate(iterator):
            complement = target - value
            i = latest_index.get(complement, sentinel)

            if i is not sentinel and nums_sum_equals(
                latest_index, value, target, complement
            ):
                return i, j

            latest_index[value] = j
    except (TypeError, ArithmeticError):
        raise TypeError(
            "nums and target must contain compatible, hashable values"
        ) from None

    raise ValueError("no pair sums to target")


def nums_sum_equals(
    latest_index: dict[Any, int],
    value: Any,
    target: Any,
    complement: Any,
) -> bool:
    """Verify arithmetic equality for a dictionary-derived candidate."""
    # The complement is used rather than retaining all previous input values:
    # dictionary equality guarantees the stored key compares equal to it.
    return complement + value == target
