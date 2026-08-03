# src/solution.py

def freq_dist(data):
    if not isinstance(data, list):
        raise ValueError("Input must be a list.")
    
    if len(data) == 0:
        raise ValueError("Data cannot be empty.")
    
    total_count = len(data)
    frequency = {}
    
    for value in data:
        if value in frequency:
            frequency[value] += 1
        else:
            frequency[value] = 1
    
    for value in frequency:
        frequency[value] = round(frequency[value] / total_count, 4)
    
    return frequency
