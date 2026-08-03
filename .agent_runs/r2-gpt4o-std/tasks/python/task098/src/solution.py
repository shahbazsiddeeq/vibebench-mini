# src/solution.py

def pearson_r(x, y):
    if len(x) != len(y):
        raise ValueError("Input lists must have the same length.")
    if len(x) < 2:
        raise ValueError("Input lists must have at least two elements.")
    
    n = len(x)
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    sum_x_diff_sq = sum((xi - mean_x) ** 2 for xi in x)
    sum_y_diff_sq = sum((yi - mean_y) ** 2 for yi in y)
    
    if sum_x_diff_sq == 0 or sum_y_diff_sq == 0:
        raise ValueError("Input lists must not have zero variance.")
    
    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    
    correlation = covariance / (sum_x_diff_sq ** 0.5 * sum_y_diff_sq ** 0.5)
    
    return round(correlation, 4)
