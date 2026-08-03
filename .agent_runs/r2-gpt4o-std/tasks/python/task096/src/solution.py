# src/solution.py

def moving_average(data, window):
    if window <= 0 or window > len(data):
        raise ValueError("Window size must be greater than 0 and less than or equal to the length of the data.")
    
    averages = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        window_average = sum(window_data) / window
        averages.append(window_average)
    
    return averages
