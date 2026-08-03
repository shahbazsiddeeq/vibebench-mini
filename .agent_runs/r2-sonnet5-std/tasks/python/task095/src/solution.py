def percentile(data, p):
    if not data:
        raise ValueError("data must not be empty")
    if p < 0 or p > 100:
        raise ValueError("p must be between 0 and 100")

    sorted_data = sorted(data)
    n = len(sorted_data)

    if n == 1:
        return float(sorted_data[0])

    rank = (p / 100) * (n - 1)
    lower_index = int(rank)
    upper_index = lower_index + 1

    if upper_index >= n:
        return float(sorted_data[-1])

    fraction = rank - lower_index
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]

    return float(lower_value + fraction * (upper_value - lower_value))
