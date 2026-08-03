"""Z-Score Normalizer module."""


def z_scores(data):
    """Return list of population z-scores for data.

    Raises ValueError if len(data) < 2 or population std == 0.
    """
    n = len(data)
    if n < 2:
        raise ValueError("data must contain at least 2 elements")

    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std = variance ** 0.5

    if std == 0:
        raise ValueError("standard deviation is zero")

    return [(x - mean) / std for x in data]
