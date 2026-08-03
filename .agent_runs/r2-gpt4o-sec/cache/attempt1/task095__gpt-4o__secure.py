# src/solution.py

from typing import List
import secrets

def percentile(data: List[float], p: float) -> float:
    if not data:
        raise ValueError("Data list cannot be empty.")
    if not (0 <= p <= 100):
        raise ValueError("Percentile must be between 0 and 100.")

    sorted_data = sorted(data)
    n = len(sorted_data)
    
    if p == 0:
        return float(sorted_data[0])
    if p == 100:
        return float(sorted_data[-1])

    rank = (p / 100) * (n - 1)
    lower_index = int(rank)
    upper_index = lower_index + 1
    weight = rank - lower_index

    if upper_index >= n:
        return float(sorted_data[lower_index])

    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]

    return float(lower_value + weight * (upper_value - lower_value))
