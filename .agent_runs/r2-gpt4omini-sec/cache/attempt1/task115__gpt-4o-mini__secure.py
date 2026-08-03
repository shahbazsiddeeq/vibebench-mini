# src/solution.py

def merge_intervals(intervals):
    # Validate input
    if not isinstance(intervals, list):
        raise ValueError("Input must be a list of intervals.")
    
    for interval in intervals:
        if not isinstance(interval, list) or len(interval) != 2:
            raise ValueError("Each interval must be a list of two elements.")
        if not all(isinstance(x, (int, float)) for x in interval):
            raise ValueError("Interval values must be integers or floats.")
        if interval[0] > interval[1]:
            raise ValueError("Start of interval must not be greater than end.")

    # Sort intervals by the start value
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    
    for current in intervals:
        if not merged:
            merged.append(current)
        else:
            last = merged[-1]
            # Check for overlap or touching intervals
            if current[0] <= last[1]:  # Overlapping or touching
                last[1] = max(last[1], current[1])  # Merge intervals
            else:
                merged.append(current)  # No overlap, add to merged list

    return merged
