# src/solution.py

def merge_intervals(intervals):
    if not intervals:
        return []
    
    # Sort the intervals based on the start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Check if there is an overlap or they touch
        if current[0] <= last_merged[1]:
            # Merge the intervals
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add the current interval
            merged.append(current)
    
    return merged
