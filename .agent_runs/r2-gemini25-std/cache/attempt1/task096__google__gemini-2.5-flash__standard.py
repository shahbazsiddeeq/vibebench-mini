def moving_average(data, window):
    """
    Calculates the simple moving average of a list of numbers.

    Args:
        data (list): A list of numbers.
        window (int): The size of the moving average window.

    Returns:
        list: A list of simple moving averages.

    Raises:
        ValueError: If window <= 0 or window > len(data).
    """
    n = len(data)

    if not isinstance(window, int) or window <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window > n:
        raise ValueError("Window size cannot be greater than the length of the data.")

    if n == 0:
        return []
    if window == 1:
        return [float(x) for x in data]

    averages = []
    current_sum = sum(data[0:window])
    averages.append(float(current_sum) / window)

    for i in range(window, n):
        current_sum += data[i] - data[i - window]
        averages.append(float(current_sum) / window)

    return averages
