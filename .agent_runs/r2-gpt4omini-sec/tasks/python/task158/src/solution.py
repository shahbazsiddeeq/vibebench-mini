# src/solution.py

from typing import List, Tuple

def linear_regression(xs: List[float], ys: List[float]) -> Tuple[float, float]:
    if len(xs) != len(ys):
        raise ValueError("Input lists must have the same length.")
    if len(xs) < 2:
        raise ValueError("At least two points are required.")
    
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sum_squares = sum((x - mx) ** 2 for x in xs)
    
    if sum_squares == 0:
        raise ValueError("All x values are identical; slope is undefined.")
    
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    return round(slope, 6), round(intercept, 6)
