def moving_average(data, window):
    if window <= 0 or window > len(data):
        raise ValueError("window must be > 0 and <= len(data)")
    result = []
    for i in range(len(data) - window + 1):
        result.append(sum(data[i:i + window]) / window)
    return result
