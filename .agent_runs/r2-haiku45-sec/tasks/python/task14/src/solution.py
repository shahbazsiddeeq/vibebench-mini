import csv
from pathlib import Path
from typing import Union


def dedupe_csv(in_path: Union[str, Path], out_path: Union[str, Path], key: str) -> int:
    """
    Read a CSV file, deduplicate by keeping only the last occurrence of each
    distinct value in the specified key column, and write to output file.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        key: Column name to deduplicate by
        
    Returns:
        Number of data rows written to output file
        
    Raises:
        KeyError: If the key column is not found in the header
    """
    in_path = Path(in_path)
    out_path = Path(out_path)
    
    # Validate inputs
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")
    
    # Read input CSV and track last occurrence of each key
    rows_by_key = {}
    fieldnames = None
    
    try:
        with in_path.open(mode='r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            
            # Check if fieldnames exist (header row present)
            if reader.fieldnames is None:
                raise KeyError(f"Column '{key}' not found in CSV header")
            
            fieldnames = reader.fieldnames
            
            # Verify key column exists
            if key not in fieldnames:
                raise KeyError(f"Column '{key}' not found in CSV header")
            
            # Read all rows, keeping track of last occurrence of each key value
            for row in reader:
                key_value = row[key]
                rows_by_key[key_value] = row
    
    except csv.Error as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    # Write output CSV with deduplicated rows in order of last occurrence
    rows_written = 0
    try:
        with out_path.open(mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write rows in the order they were last seen
            for row in rows_by_key.values():
                writer.writerow(row)
                rows_written += 1
    
    except IOError as e:
        raise IOError(f"Error writing to output file: {e}")
    
    return rows_written
