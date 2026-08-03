def merge_intervals(intervals):
    """
    Merge overlapping or touching intervals.
    
    Args:
        intervals: List of [start, end] pairs
        
    Returns:
        List of merged [start, end] pairs, sorted by start
    """
    if not intervals:
        return []
    
    # Sort intervals by start position
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # Initialize merged list with first interval
    merged = [sorted_intervals[0]]
    
    # Iterate through remaining intervals
    for current in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps or touches the last merged interval
        if current[0] <= last_merged[1]:
            # Merge by extending the end of the last interval
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add as new interval
            merged.append(current)
    
    return merged
