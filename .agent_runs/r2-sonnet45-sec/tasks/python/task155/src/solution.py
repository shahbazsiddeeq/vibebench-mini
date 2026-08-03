def group_by_aggregate(records, key_field, value_field):
    """
    Group records by key_field and aggregate values from value_field.
    
    Args:
        records: List of dictionaries
        key_field: Field name to group by
        value_field: Field name containing numeric values to aggregate
    
    Returns:
        Dict mapping each group key to {'count': int, 'sum': float, 'mean': float}
        
    Raises:
        KeyError: If any record is missing key_field or value_field
    """
    if not records:
        return {}
    
    # Validate inputs
    if not isinstance(records, list):
        raise TypeError("records must be a list")
    if not isinstance(key_field, str):
        raise TypeError("key_field must be a string")
    if not isinstance(value_field, str):
        raise TypeError("value_field must be a string")
    
    groups = {}
    
    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Each record must be a dictionary")
        
        # Access fields - let KeyError propagate if missing
        group_key = record[key_field]
        value = record[value_field]
        
        # Validate value is numeric
        if not isinstance(value, (int, float)):
            raise TypeError(f"Value field must contain numeric data, got {type(value)}")
        
        # Initialize group if not exists
        if group_key not in groups:
            groups[group_key] = {
                'count': 0,
                'sum': 0.0,
                'values': []
            }
        
        # Accumulate
        groups[group_key]['count'] += 1
        groups[group_key]['sum'] += float(value)
        groups[group_key]['values'].append(float(value))
    
    # Calculate means and prepare output
    result = {}
    for key, data in groups.items():
        count = data['count']
        total_sum = data['sum']
        mean = round(total_sum / count, 4)
        
        result[key] = {
            'count': count,
            'sum': total_sum,
            'mean': mean
        }
    
    return result
