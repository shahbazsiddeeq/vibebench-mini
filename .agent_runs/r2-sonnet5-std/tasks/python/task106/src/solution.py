def histogram(data, bins):
    if bins < 1:
        raise ValueError("bins must be >= 1")
    if not data:
        raise ValueError("data must not be empty")

    lo = float(min(data))
    hi = float(max(data))

    if lo == hi:
        return [(lo, hi, len(data))]

    width = (hi - lo) / bins
    edges = [lo + i * width for i in range(bins + 1)]
    edges[-1] = hi  # ensure exact final edge

    counts = [0] * bins
    for x in data:
        x = float(x)
        if x == hi:
            counts[-1] += 1
            continue
        idx = int((x - lo) / width)
        if idx < 0:
            idx = 0
        if idx >= bins:
            idx = bins - 1
        counts[idx] += 1

    return [(edges[i], edges[i + 1], counts[i]) for i in range(bins)]
