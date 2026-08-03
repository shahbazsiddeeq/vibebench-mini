def moving_average(data, window):
    if window <= 0:
        raise ValueError("Window size must be greater than 0.")
    if window > len(data):
        raise ValueError("Window size must not be greater than the length of the data.")
    
    averages = []
    for i in range(len(data) - window + 1):
        window_sum = sum(data[i:i + window])
        averages.append(window_sum / window)
    
    return averages
