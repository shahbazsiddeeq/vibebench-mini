def merge_intervals(intervals):
    """
    Merge overlapping or touching intervals.
    
    Args:
        intervals: A list of [start, end] pairs
        
    Returns:
        A list of merged, non-overlapping [start, end] lists, sorted by start
    """
    # Handle empty input
    if not intervals:
        return []
    
    # Validate input is a list
    if not isinstance(intervals, list):
        raise TypeError("intervals must be a list")
    
    # Validate each interval
    validated_intervals = []
    for interval in intervals:
        # Check if interval is a list or tuple with exactly 2 elements
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValueError("Each interval must be a list or tuple with exactly 2 elements")
        
        start, end = interval
        
        # Validate that start and end are numbers
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise TypeError("Interval start and end must be numbers")
        
        # Validate that start <= end
        if start > end:
            raise ValueError("Interval start must be <= end")
        
        validated_intervals.append([start, end])
    
    # Sort intervals by start time
    sorted_intervals = sorted(validated_intervals, key=lambda x: x[0])
    
    # Merge overlapping or touching intervals
    merged = [sorted_intervals[0]]
    
    for current in sorted_intervals[1:]:
        last_merged = merged[-1]
        
        # Check if current interval overlaps or touches the last merged interval
        # Overlapping: current[0] <= last_merged[1]
        # Touching: current[0] == last_merged[1]
        if current[0] <= last_merged[1]:
            # Merge by extending the end of the last merged interval
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add current interval to merged list
            merged.append(current)
    
    return merged
