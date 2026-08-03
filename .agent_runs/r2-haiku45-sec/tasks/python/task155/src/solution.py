def group_by_aggregate(records, key_field, value_field):
    """
    Group records by key_field and aggregate numeric values at value_field.
    
    Args:
        records: List of dictionaries
        key_field: Field name to group by
        value_field: Field name containing numeric values to aggregate
    
    Returns:
        Dict mapping group keys to dicts with 'count', 'sum', and 'mean'
    
    Raises:
        KeyError: If any record is missing key_field or value_field
    """
    if not records:
        return {}
    
    groups = {}
    
    for record in records:
        # Let KeyError propagate if fields are missing
        key = record[key_field]
        value = record[value_field]
        
        # Initialize group if not seen before
        if key not in groups:
            groups[key] = {
                'count': 0,
                'sum': 0.0,
                'values': []
            }
        
        # Aggregate the value
        groups[key]['count'] += 1
        groups[key]['sum'] += float(value)
        groups[key]['values'].append(float(value))
    
    # Calculate means and format output
    result = {}
    for key, group_data in groups.items():
        count = group_data['count']
        total_sum = group_data['sum']
        mean = round(total_sum / count, 4)
        
        result[key] = {
            'count': count,
            'sum': total_sum,
            'mean': mean
        }
    
    return result
