import collections

def moving_average(data, window):
    """
    Calculates the simple moving average of a list of numbers.

    Args:
        data (list): A list of numbers (integers or floats).
        window (int): The size of the moving average window.

    Returns:
        list: A list of floats representing the simple moving averages.

    Raises:
        ValueError: If window is less than or equal to 0, or if window is
                    greater than the length of the data.
        TypeError: If data is not a list, or if window is not an integer,
                   or if elements in data are not numbers.
    """
    if not isinstance(data, list):
        raise TypeError("Input 'data' must be a list.")
    if not isinstance(window, int):
        raise TypeError("Input 'window' must be an integer.")

    n = len(data)

    if window <= 0:
        raise ValueError("Window size must be greater than 0.")
    if window > n:
        raise ValueError("Window size cannot be greater than the length of the data.")

    # Validate data elements are numbers
    for i, item in enumerate(data):
        if not isinstance(item, (int, float)):
            raise TypeError(f"All elements in 'data' must be numbers (int or float), "
                            f"found type {type(item).__name__} at index {i}.")

    if n == 0:
        return []

    averages = []
    current_sum = 0.0

    # Calculate the sum for the first window
    for i in range(window):
        current_sum += float(data[i])
    averages.append(current_sum / window)

    # Slide the window and update the sum
    for i in range(window, n):
        current_sum += float(data[i]) - float(data[i - window])
        averages.append(current_sum / window)

    return averages
