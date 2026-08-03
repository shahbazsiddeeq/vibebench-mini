def histogram(data, bins):
    """
    Calculates a histogram for the given data with a specified number of equal-width bins.

    Args:
        data (list): A list of numerical data (integers or floats).
        bins (int): The number of bins to use. Must be a positive integer.

    Returns:
        list: A list of (bin_start, bin_end, count) tuples. Each bin is half-open
              [bin_start, bin_end) except for the last bin which is closed [bin_start, bin_end].

    Raises:
        ValueError: If 'data' is empty, 'bins' is less than 1, or 'data' contains non-numeric values.
    """
    if not isinstance(data, list):
        raise ValueError("Data must be a list.")
    if not data:
        raise ValueError("Data cannot be empty.")
    if not isinstance(bins, int):
        raise ValueError("Bins must be an integer.")
    if bins < 1:
        raise ValueError("Number of bins must be at least 1.")

    # Validate data elements are numeric
    for item in data:
        if not isinstance(item, (int, float)):
            raise ValueError("All data elements must be numeric (int or float).")

    min_val = float(min(data))
    max_val = float(max(data))

    if min_val == max_val:
        # All values are the same, return a single bin
        return [(min_val, max_val, len(data))]

    # Calculate bin width
    # Add a small epsilon to max_val to ensure max_val falls into the last bin
    # when max_val is exactly an upper bound of a bin.
    # This handles cases like data=[0,1,2,3], bins=2 where max_val=3.0 and bin_width=1.5.
    # Without epsilon, 3.0 might be exactly on the boundary of the last bin,
    # and due to floating point inaccuracies, might be excluded.
    # The problem statement says "the final bin is closed [bin_start, bin_end] so max(data) is counted."
    # This epsilon approach ensures max_val is always included in the last bin.
    bin_width = (max_val - min_val) / bins

    # Initialize bins
    histogram_bins = [(0.0, 0.0, 0) for _ in range(bins)]

    # Determine bin edges
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        histogram_bins[i] = (bin_start, bin_end, 0)

    # Count elements in each bin
    for value in data:
        # Determine which bin the value belongs to
        if value == max_val:
            # Ensure max_val always falls into the last bin
            bin_index = bins - 1
        else:
            # Calculate bin index for other values
            bin_index = int((value - min_val) / bin_width)
            # Handle potential floating point issues where value might be slightly
            # less than min_val due to precision, or slightly greater than
            # the upper bound of the last bin (excluding max_val).
            # Ensure bin_index is within valid range [0, bins-1].
            if bin_index < 0:
                bin_index = 0
            elif bin_index >= bins:
                bin_index = bins - 1 # Should not happen with the max_val check above, but for safety

        current_start, current_end, current_count = histogram_bins[bin_index]
        histogram_bins[bin_index] = (current_start, current_end, current_count + 1)

    return histogram_bins
