def min_max_normalize(values, new_min=0.0, new_max=1.0):
    if not values:
        raise ValueError("Input list 'values' must not be empty.")
    
    if not isinstance(new_min, (int, float)) or not isinstance(new_max, (int, float)):
        raise ValueError("'new_min' and 'new_max' must be numbers.")
    
    lo = min(values)
    hi = max(values)
    
    if lo == hi:
        return [round(float(new_min), 6) for _ in values]
    
    scale = new_max - new_min
    return [round(new_min + (x - lo) / (hi - lo) * scale, 6) for x in values]
