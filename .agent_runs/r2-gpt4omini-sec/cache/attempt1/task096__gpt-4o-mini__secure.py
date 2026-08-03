# src/solution.py

def moving_average(data, window):
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Data must be a list of numbers.")
    if not isinstance(window, int) or window <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window > len(data):
        raise ValueError("Window size must not be greater than the length of the data.")

    averages = []
    for i in range(len(data) - window + 1):
        window_sum = sum(data[i:i + window])
        averages.append(window_sum / window)

    return averages
