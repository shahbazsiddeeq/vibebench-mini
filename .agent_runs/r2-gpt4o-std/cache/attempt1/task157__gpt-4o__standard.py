def min_max_normalize(values, new_min=0.0, new_max=1.0):
    if not values:
        raise ValueError("The input list 'values' must not be empty.")
    
    lo = min(values)
    hi = max(values)
    
    if lo == hi:
        return [round(float(new_min), 6) for _ in values]
    
    scale = new_max - new_min
    return [round(new_min + (x - lo) / (hi - lo) * scale, 6) for x in values]
