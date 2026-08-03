def merge_intervals(intervals):
    if not isinstance(intervals, list):
        raise ValueError("Input must be a list of intervals.")
    
    for interval in intervals:
        if not (isinstance(interval, list) and len(interval) == 2 and 
                all(isinstance(x, (int, float)) for x in interval)):
            raise ValueError("Each interval must be a list of two numbers.")
    
    # Sort intervals by the start time
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    
    return merged
