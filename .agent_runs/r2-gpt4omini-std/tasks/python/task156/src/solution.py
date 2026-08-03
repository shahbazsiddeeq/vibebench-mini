# src/solution.py

def weighted_average(values, weights):
    if not values or not weights:
        raise ValueError("Values and weights must not be empty.")
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Sum of weights must not be zero.")
    
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    return round(weighted_sum / total_weight, 6)
