def linear_regression(xs, ys):
    if not isinstance(xs, list) or not isinstance(ys, list):
        raise ValueError("Inputs must be lists.")
    
    if len(xs) != len(ys):
        raise ValueError("Input lists must have the same length.")
    
    n = len(xs)
    if n < 2:
        raise ValueError("At least two points are required.")
    
    try:
        mx = sum(xs) / n
        my = sum(ys) / n
    except TypeError:
        raise ValueError("Lists must contain numerical values.")
    
    sum_prod = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sum_sq = sum((x - mx) ** 2 for x in xs)
    
    if sum_sq == 0:
        raise ValueError("All x values are identical; slope is undefined.")
    
    slope = sum_prod / sum_sq
    intercept = my - slope * mx
    
    return round(slope, 6), round(intercept, 6)
