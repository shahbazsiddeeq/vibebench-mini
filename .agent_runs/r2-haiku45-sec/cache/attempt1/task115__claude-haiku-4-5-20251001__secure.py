def merge_intervals(intervals):
    """
    Merge overlapping or touching intervals.
    
    Args:
        intervals: A list of [start, end] pairs
        
    Returns:
        A list of merged, non-overlapping [start, end] pairs sorted by start
    """
    # Input validation
    if not isinstance(intervals, list):
        raise TypeError("intervals must be a list")
    
    # Handle empty list
    if not intervals:
        return []
    
    # Validate and convert intervals to a list of tuples for processing
    validated_intervals = []
    for interval in intervals:
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValueError("Each interval must be a [start, end] pair")
        
        start, end = interval
        
        # Validate that start and end are numbers
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise TypeError("Interval start and end must be numeric")
        
        # Validate that start <= end
        if start > end:
            raise ValueError(f"Invalid interval: start ({start}) must be <= end ({end})")
        
        validated_intervals.append((start, end))
    
    # Sort intervals by start time, then by end time
    sorted_intervals = sorted(validated_intervals, key=lambda x: (x[0], x[1]))
    
    # Merge overlapping intervals
    merged = []
    for current_start, current_end in sorted_intervals:
        if merged and current_start <= merged[-1][1]:
            # Overlapping or touching: merge by extending the end of the last interval
            merged[-1] = (merged[-1][0], max(merged[-1][1], current_end))
        else:
            # Non-overlapping: add as new interval
            merged.append((current_start, current_end))
    
    # Convert back to list format
    return [[start, end] for start, end in merged]
