def histogram(data: list[float], bins: int) -> list[tuple[float, float, int]]:
    if bins < 1:
        raise ValueError("bins must be >= 1")
    if not data:
        raise ValueError("data must not be empty")
    min_val = float(min(data))
    max_val = float(max(data))
    if min_val == max_val:
        return [(min_val, max_val, len(data))]
    width = (max_val - min_val) / bins
    result = []
    for i in range(bins):
        lo = min_val + i * width
        if i == bins - 1:
            hi = max_val
            count = sum(1 for x in data if lo <= x <= max_val)
        else:
            hi = min_val + (i + 1) * width
            count = sum(1 for x in data if lo <= x < hi)
        result.append((lo, hi, count))
    return result
