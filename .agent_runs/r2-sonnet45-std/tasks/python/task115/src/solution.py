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
    
    # Sort intervals by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    # Initialize result with first interval
    merged = [sorted_intervals[0]]
    
    for current in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps or touches the last merged interval
        # Overlap/touch condition: current start <= last end
        if current[0] <= last_merged[1]:
            # Merge by extending the end of the last merged interval
            merged[-1] = [last_merged[0], max(last_merged[1], current[1])]
        else:
            # No overlap, add current interval as new
            merged.append(current)
    
    return merged
