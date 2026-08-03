# src/solution.py

def pearson_r(x, y):
    if len(x) != len(y):
        raise ValueError("Input lists must have the same length.")
    if len(x) < 2:
        raise ValueError("Input lists must contain at least two elements.")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    sum_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_xx = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_yy = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    if sum_xx == 0 or sum_yy == 0:
        raise ValueError("Input lists must not have zero variance.")
    
    r = sum_xy / (sum_xx ** 0.5 * sum_yy ** 0.5)
    return round(r, 4)
