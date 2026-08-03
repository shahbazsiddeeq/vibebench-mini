# src/solution.py

def linear_regression(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("Input lists must have the same length.")
    if len(xs) < 2:
        raise ValueError("At least two points are required.")
    
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sum_squares = sum((x - mx) ** 2 for x in xs)
    
    if sum_squares == 0:
        raise ValueError("All x values are identical; slope is undefined.")
    
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    return round(slope, 6), round(intercept, 6)
