def histogram(data, bins):
    if not data:
        raise ValueError("data cannot be empty")
    if bins < 1:
        raise ValueError("bins must be at least 1")

    min_val = float(min(data))
    max_val = float(max(data))

    if min_val == max_val:
        return [(min_val, max_val, len(data))]

    # Calculate bin width
    # To ensure max_val is included in the last bin, we slightly adjust the range
    # if max_val is not exactly on a bin edge.
    # This is crucial for floating point precision and the half-open/closed bin definition.
    bin_width = (max_val - min_val) / bins

    # If max_val is exactly on a bin boundary, and it's not the min_val itself,
    # we need to slightly increase the bin_width to ensure max_val falls into the last bin
    # when using the half-open interval [start, end).
    # This check is important for cases like data=[0,1,2,3], bins=2 where bin_width=1.5.
    # The last bin would be [1.5, 3.0). If max_val is 3.0, it would be excluded.
    # A small epsilon is added to the upper bound of the range for calculation.
    # However, the problem statement implies the last bin is closed, so we handle that explicitly.

    # Initialize bins
    histogram_bins = []
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        histogram_bins.append([bin_start, bin_end, 0]) # Use list for mutable count

    # Count data points into bins
    for x in data:
        # Handle the special case for the maximum value to ensure it falls into the last bin
        if x == max_val:
            # If there's only one bin, it's already handled by the min_val == max_val case.
            # If multiple bins, max_val must go into the last bin.
            histogram_bins[bins - 1][2] += 1
        else:
            # For all other values, determine the bin index
            # Use max(0, ...) to handle potential floating point inaccuracies that might
            # result in a slightly negative index for values very close to min_val.
            # Use min(bins - 1, ...) to ensure index doesn't exceed bounds for values
            # very close to max_val but not exactly max_val.
            bin_index = int((x - min_val) / bin_width)
            bin_index = max(0, min(bin_index, bins - 1))
            histogram_bins[bin_index][2] += 1

    # Convert to tuples
    return [tuple(b) for b in histogram_bins]
