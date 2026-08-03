def group_by_aggregate(records, key_field, value_field):
    """
    Groups records by a key_field and aggregates numeric values from value_field.

    Args:
        records (list): A list of dictionaries, where each dictionary represents a record.
        key_field (str): The key to use for grouping records.
        value_field (str): The key whose numeric values will be aggregated.

    Returns:
        dict: A dictionary where keys are group keys and values are dictionaries
              containing 'count', 'sum', and 'mean' for that group.
              'sum' and 'mean' are always floats. 'mean' is rounded to 4 decimal places.
              Returns an empty dict if records is empty.
    """
    if not records:
        return {}

    grouped_data = {}

    for record in records:
        key = record[key_field]
        value = float(record[value_field])  # Ensure value is float for sum

        if key not in grouped_data:
            grouped_data[key] = {'count': 0, 'sum': 0.0}
        
        grouped_data[key]['count'] += 1
        grouped_data[key]['sum'] += value

    result = {}
    for key, data in grouped_data.items():
        count = data['count']
        total_sum = data['sum']
        mean = round(total_sum / count, 4) if count > 0 else 0.0 # Handle division by zero, though count will always be > 0 here

        result[key] = {
            'count': count,
            'sum': total_sum,
            'mean': mean
        }
    
    return result
