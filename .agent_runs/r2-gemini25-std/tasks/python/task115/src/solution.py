def merge_intervals(intervals):
    """
    Merges a list of [start, end] pairs into a list of non-overlapping intervals.

    Args:
        intervals: A list of [start, end] lists, representing intervals.

    Returns:
        A list of merged, non-overlapping intervals, sorted by start (ascending).
        Returns an empty list if the input is empty.
    """
    if not intervals:
        return []

    # Sort the intervals by their start times
    intervals.sort(key=lambda x: x[0])

    merged = []
    for interval in intervals:
        # If the merged list is empty or the current interval does not overlap
        # with the previous merged interval, append it directly.
        # Overlap includes touching: [1,3] and [3,5] -> [1,5]
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            # Otherwise, there is an overlap (or touching), so merge the current
            # and previous intervals by updating the end of the previous interval.
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged
