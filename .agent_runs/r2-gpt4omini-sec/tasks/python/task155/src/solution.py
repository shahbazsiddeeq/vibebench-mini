# src/solution.py

def group_by_aggregate(records, key_field, value_field):
    if not isinstance(records, list):
        raise ValueError("Records must be a list.")
    
    result = {}
    
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each record must be a dictionary.")
        
        if key_field not in record or value_field not in record:
            raise KeyError(f"Missing field in record: {record}")
        
        key = record[key_field]
        value = record[value_field]
        
        if key not in result:
            result[key] = {'count': 0, 'sum': 0.0}
        
        result[key]['count'] += 1
        result[key]['sum'] += float(value)
    
    for key, aggregates in result.items():
        aggregates['mean'] = round(aggregates['sum'] / aggregates['count'], 4)
    
    return result
