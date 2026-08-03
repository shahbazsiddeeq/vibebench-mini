import secrets

def weighted_average(values, weights):
    # Validate inputs
    if not values or not weights:
        raise ValueError("Values and weights must not be empty.")
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    
    # Calculate the sum of weights
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Sum of weights must not be zero.")
    
    # Calculate the weighted sum
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    
    # Calculate the weighted average
    weighted_avg = weighted_sum / total_weight
    
    # Return the result rounded to 6 decimal places
    return round(weighted_avg, 6)
