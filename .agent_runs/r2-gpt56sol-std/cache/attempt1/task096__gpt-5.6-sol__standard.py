"""Utilities for calculating moving averages."""


def moving_average(data, window):
    """Return simple moving averages over consecutive windows of *data*."""
    values = list(data)

    if not isinstance(window, int) or isinstance(window, bool):
        raise TypeError("window must be an integer")
    if window <= 0 or window > len(values):
        raise ValueError("window must be positive and no greater than data length")

    current_sum = sum(values[:window])
    averages = [current_sum / window]

    for index in range(window, len(values)):
        current_sum += values[index] - values[index - window]
        averages.append(current_sum / window)

    return averages
