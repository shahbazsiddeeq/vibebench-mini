import csv
from pathlib import Path


def dedupe_csv(in_path, out_path, key):
    """
    Reads a CSV with a header row and writes a CSV keeping only the last 
    occurrence of each distinct value in column `key`.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        key: Column name to use for deduplication
        
    Returns:
        Number of data rows written
        
    Raises:
        KeyError: If the key column is absent from the header
    """
    # Validate inputs
    if not isinstance(in_path, (str, Path)):
        raise TypeError("in_path must be a string or Path")
    if not isinstance(out_path, (str, Path)):
        raise TypeError("out_path must be a string or Path")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    # Read all rows and track last occurrence
    rows_by_key = {}  # key_value -> (last_position, row_dict)
    fieldnames = None
    
    try:
        with open(in_path, 'r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            
            # Get fieldnames (header)
            fieldnames = reader.fieldnames
            
            # Check if header exists and key is present
            if fieldnames is None:
                raise KeyError(f"Key '{key}' not found in CSV header")
            
            if key not in fieldnames:
                raise KeyError(f"Key '{key}' not found in CSV header")
            
            # Read all rows, keeping track of last occurrence
            position = 0
            for row in reader:
                key_value = row.get(key)
                # Store the row with its position (last occurrence wins)
                rows_by_key[key_value] = (position, row)
                position += 1
    
    except FileNotFoundError:
        raise
    except csv.Error:
        raise
    
    # Sort by last occurrence position
    sorted_rows = sorted(rows_by_key.values(), key=lambda x: x[0])
    
    # Write output
    try:
        with open(out_path, 'w', encoding='utf-8', newline='') as outfile:
            if fieldnames:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for _, row in sorted_rows:
                    writer.writerow(row)
    
    except (IOError, OSError):
        raise
    
    return len(sorted_rows)
