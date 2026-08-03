# src/solution.py

from typing import List

def moving_average(data: List[float], window: int) -> List[float]:
    if not isinstance(window, int) or window <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window > len(data):
        raise ValueError("Window size must not be greater than the length of the data.")
    
    averages = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        window_average = sum(window_data) / window
        averages.append(window_average)
    
    return averages
