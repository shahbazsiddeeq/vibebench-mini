# src/solution.py

def percentile(data, p):
    if not data:
        raise ValueError("Data cannot be empty.")
    if not (0 <= p <= 100):
        raise ValueError("Percentile must be between 0 and 100.")

    data = sorted(data)
    n = len(data)
    rank = (p / 100) * (n - 1)
    lower_index = int(rank)
    upper_index = lower_index + 1

    if upper_index >= n:
        return float(data[lower_index])

    lower_value = data[lower_index]
    upper_value = data[upper_index]
    fraction = rank - lower_index

    return lower_value + (upper_value - lower_value) * fraction
