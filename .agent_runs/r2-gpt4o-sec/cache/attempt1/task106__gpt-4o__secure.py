def histogram(data, bins):
    if not data:
        raise ValueError("Data cannot be empty.")
    if bins < 1:
        raise ValueError("Number of bins must be at least 1.")

    min_val = min(data)
    max_val = max(data)

    if min_val == max_val:
        return [(min_val, max_val, len(data))]

    bin_width = (max_val - min_val) / bins
    bin_edges = [min_val + i * bin_width for i in range(bins + 1)]
    bin_edges[-1] = max_val  # Ensure the last bin is closed

    counts = [0] * bins

    for value in data:
        if value == max_val:
            counts[-1] += 1
        else:
            index = int((value - min_val) / bin_width)
            counts[index] += 1

    result = [(bin_edges[i], bin_edges[i + 1], counts[i]) for i in range(bins)]
    return result
