# src/solution.py

from typing import List
import secrets

def percentile(data: List[float], p: float) -> float:
    if not data:
        raise ValueError("Data cannot be empty.")
    if not (0 <= p <= 100):
        raise ValueError("Percentile must be between 0 and 100.")

    # Sort the data to calculate the percentile correctly
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # Calculate the rank
    rank = (p / 100) * (n - 1)
    lower_index = int(rank)
    upper_index = lower_index + 1

    if upper_index >= n:  # If rank is at the end of the list
        return float(sorted_data[lower_index])

    # Linear interpolation
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    interpolation = lower_value + (upper_value - lower_value) * (rank - lower_index)

    return interpolation
