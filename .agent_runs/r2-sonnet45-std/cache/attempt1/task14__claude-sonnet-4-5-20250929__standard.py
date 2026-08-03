import csv


def dedupe_csv(in_path, out_path, key):
    """
    Reads a CSV with a header row and writes a CSV keeping only the last occurrence
    of each distinct value in column `key`.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        key: Column name to use for deduplication
    
    Returns:
        Number of data rows written
    
    Raises:
        KeyError: If the key column is not in the header
    """
    # Read all rows and track the last occurrence of each key value
    with open(in_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        
        # Check if key exists in fieldnames
        if reader.fieldnames is None or key not in reader.fieldnames:
            raise KeyError(key)
        
        fieldnames = reader.fieldnames
        
        # Dictionary to store the last occurrence of each key value
        # Maps key_value -> (row_dict, last_position)
        last_occurrences = {}
        position = 0
        
        for row in reader:
            key_value = row[key]
            last_occurrences[key_value] = (row, position)
            position += 1
    
    # Sort by the position of last occurrence
    sorted_rows = sorted(last_occurrences.values(), key=lambda x: x[1])
    
    # Write output
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row, _ in sorted_rows:
            writer.writerow(row)
    
    return len(sorted_rows)
