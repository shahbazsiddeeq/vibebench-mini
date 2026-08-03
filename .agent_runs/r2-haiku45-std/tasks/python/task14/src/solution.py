import csv
from typing import Dict, List, Tuple


def dedupe_csv(in_path: str, out_path: str, key: str) -> int:
    """
    Read a CSV file, deduplicate by keeping only the last occurrence of each
    key value, and write to output file.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        key: Column name to deduplicate by
        
    Returns:
        Number of data rows written to output
        
    Raises:
        KeyError: If the key column is not in the header
    """
    # Read input CSV
    with open(in_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Check if header exists and key is present
        if reader.fieldnames is None:
            raise KeyError(key)
        
        if key not in reader.fieldnames:
            raise KeyError(key)
        
        # Track last occurrence of each key value
        # Store: {key_value: (row_dict, position)}
        last_occurrences: Dict[str, Tuple[Dict, int]] = {}
        position = 0
        
        for row in reader:
            key_value = row[key]
            last_occurrences[key_value] = (row, position)
            position += 1
        
        # Sort by position of last occurrence
        sorted_rows = sorted(
            last_occurrences.values(),
            key=lambda x: x[1]
        )
        
        # Write output CSV
        with open(out_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            for row_dict, _ in sorted_rows:
                writer.writerow(row_dict)
        
        return len(sorted_rows)
