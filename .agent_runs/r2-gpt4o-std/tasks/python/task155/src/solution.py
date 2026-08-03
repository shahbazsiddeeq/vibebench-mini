def group_by_aggregate(records, key_field, value_field):
    from collections import defaultdict

    # Initialize a dictionary to hold the aggregated data
    groups = defaultdict(lambda: {'count': 0, 'sum': 0.0})

    # Iterate over each record
    for record in records:
        # Extract the key and value using the provided field names
        key = record[key_field]
        value = record[value_field]

        # Update the group's count and sum
        groups[key]['count'] += 1
        groups[key]['sum'] += float(value)

    # Prepare the final result with mean calculation
    result = {}
    for key, data in groups.items():
        count = data['count']
        total_sum = data['sum']
        mean = round(total_sum / count, 4)
        result[key] = {'count': count, 'sum': total_sum, 'mean': mean}

    return result
