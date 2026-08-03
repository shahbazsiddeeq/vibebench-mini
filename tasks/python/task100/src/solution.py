def freq_dist(data: list) -> dict:
    if not data:
        raise ValueError("data must not be empty")
    counts = {}
    for item in data:
        counts[item] = counts.get(item, 0) + 1
    n = len(data)
    return {value: round(count / n, 4) for value, count in counts.items()}
