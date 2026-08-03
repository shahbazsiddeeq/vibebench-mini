# src/solution.py

def freq_dist(data):
    if not data:
        raise ValueError("Data cannot be empty")
    
    total_count = len(data)
    frequency = {}
    
    for item in data:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    
    for key in frequency:
        frequency[key] = round(frequency[key] / total_count, 4)
    
    return frequency
