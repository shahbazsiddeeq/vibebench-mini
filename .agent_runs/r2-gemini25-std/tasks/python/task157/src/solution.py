def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """
    Rescales a list of numbers to a target range using min-max scaling.

    For each element x the scaled value is new_min + (x - lo) / (hi - lo) * (new_max - new_min),
    where lo = min(values) and hi = max(values).

    Args:
        values (list): A list of numbers to be normalized.
        new_min (float): The desired minimum value of the scaled range. Defaults to 0.0.
        new_max (float): The desired maximum value of the scaled range. Defaults to 1.0.

    Returns:
        list: A new list of floats, each rounded to 6 decimal places.

    Raises:
        ValueError: If `values` is empty.
    """
    if not values:
        raise ValueError("Input list 'values' cannot be empty.")

    lo = min(values)
    hi = max(values)

    normalized_values = []

    if hi == lo:
        # Special case for a constant series or single-element list
        for _ in values:
            normalized_values.append(round(float(new_min), 6))
    else:
        # Calculate the scaling factor for the new range
        scale_factor = (new_max - new_min) / (hi - lo)
        for x in values:
            scaled_value = new_min + (x - lo) * scale_factor
            normalized_values.append(round(scaled_value, 6))

    return normalized_values
