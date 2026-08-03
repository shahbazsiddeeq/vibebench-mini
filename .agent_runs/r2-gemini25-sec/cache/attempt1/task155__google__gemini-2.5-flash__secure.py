def group_by_aggregate(records: list[dict], key_field: str, value_field: str) -> dict:
    """
    Groups records by a key_field and aggregates numeric values from a value_field.

    Args:
        records: A list of dictionaries, where each dictionary represents a record.
        key_field: The string key to group records by.
        value_field: The string key whose numeric values will be aggregated.

    Returns:
        A dictionary where keys are the group keys and values are dictionaries
        containing 'count', 'sum', and 'mean' for each group.
        Returns an empty dictionary if records is empty.

    Raises:
        KeyError: If any record is missing key_field or value_field.
        TypeError: If the value at value_field is not a number (int or float).
    """
    if not isinstance(records, list):
        raise TypeError("records must be a list")
    if not isinstance(key_field, str):
        raise TypeError("key_field must be a string")
    if not isinstance(value_field, str):
        raise TypeError("value_field must be a string")

    if not records:
        return {}

    grouped_data = {}

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Each record in 'records' must be a dictionary")

        # KeyError will propagate if fields are missing, as per requirements
        key = record[key_field]
        value = record[value_field]

        if not isinstance(value, (int, float)):
            raise TypeError(f"Value for '{value_field}' must be a number, got {type(value)}")

        if key not in grouped_data:
            grouped_data[key] = {'count': 0, 'sum': 0.0}

        grouped_data[key]['count'] += 1
        grouped_data[key]['sum'] += float(value)

    result = {}
    for key, data in grouped_data.items():
        count = data['count']
        total_sum = data['sum']
        mean = round(total_sum / count, 4) if count > 0 else 0.0
        result[key] = {'count': count, 'sum': total_sum, 'mean': mean}

    return result
