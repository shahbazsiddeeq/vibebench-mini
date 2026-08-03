# src/solution.py

def weighted_average(values, weights):
    # Validate inputs
    if not isinstance(values, list) or not isinstance(weights, list):
        raise ValueError("Both values and weights must be lists.")
    
    if len(values) == 0 or len(weights) == 0:
        raise ValueError("Values and weights cannot be empty.")
    
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    
    # Calculate the total weight
    total_weight = sum(weights)
    
    if total_weight == 0:
        raise ValueError("Sum of weights cannot be zero.")
    
    # Calculate the weighted average
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    average = weighted_sum / total_weight
    
    # Return the result rounded to 6 decimal places
    return round(average, 6)
