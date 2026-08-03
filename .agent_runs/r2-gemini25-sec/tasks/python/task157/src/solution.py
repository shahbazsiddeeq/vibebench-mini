def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """
    Rescales a list of numbers to a target range using min-max scaling.

    For each element x, the scaled value is new_min + (x - lo) / (hi - lo) * (new_max - new_min),
    where lo = min(values) and hi = max(values).

    Args:
        values (list): A list of numbers (integers or floats) to be normalized.
        new_min (float): The desired minimum value of the scaled data. Defaults to 0.0.
        new_max (float): The desired maximum value of the scaled data. Defaults to 1.0.

    Returns:
        list: A new list of floats, each rounded to 6 decimal places, representing
              the normalized values.

    Raises:
        ValueError: If `values` is empty.
        TypeError: If `values` is not a list or contains non-numeric types,
                   or if new_min/new_max are not numeric.
    """
    if not isinstance(values, list):
        raise TypeError("Input 'values' must be a list.")
    if not values:
        raise ValueError("Input 'values' cannot be empty.")
    if not all(isinstance(x, (int, float)) for x in values):
        raise TypeError("All elements in 'values' must be numbers.")
    if not isinstance(new_min, (int, float)) or not isinstance(new_max, (int, float)):
        raise TypeError("'new_min' and 'new_max' must be numbers.")

    lo = min(values)
    hi = max(values)

    normalized_values = []

    if hi == lo:
        # Special case for a constant series or single-element list
        for _ in values:
            normalized_values.append(round(float(new_min), 6))
    else:
        # Calculate the scaling factor
        scale_factor = (new_max - new_min) / (hi - lo)
        for x in values:
            scaled_value = new_min + (x - lo) * scale_factor
            normalized_values.append(round(scaled_value, 6))

    return normalized_values
