# src/solution.py

def freq_dist(data):
    if not data:
        raise ValueError("Data cannot be empty")
    
    total_count = len(data)
    frequency = {}
    
    for value in data:
        frequency[value] = frequency.get(value, 0) + 1
    
    for value in frequency:
        frequency[value] = round(frequency[value] / total_count, 4)
    
    return frequency
