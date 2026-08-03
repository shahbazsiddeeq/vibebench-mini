import csv
from pathlib import Path


def csv_filter(in_path, out_path, column, value):
    """
    Filter CSV rows by column value and write matching rows to output file.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        column: Column name to filter by
        value: Value to match in the specified column
        
    Returns:
        Count of data rows written (excluding header)
        
    Raises:
        KeyError: If column not found in CSV header
        FileNotFoundError: If input file doesn't exist
        IOError: If there are issues reading/writing files
    """
    # Validate inputs
    if not isinstance(in_path, str):
        raise TypeError("in_path must be a string")
    if not isinstance(out_path, str):
        raise TypeError("out_path must be a string")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    
    # Check that input file exists
    in_file = Path(in_path)
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")
    
    count = 0
    fieldnames = None
    
    try:
        # Read input CSV and collect matching rows
        with open(in_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Check if column exists in header
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no header")
            
            if column not in reader.fieldnames:
                raise KeyError(f"Column '{column}' not found in CSV header")
            
            fieldnames = reader.fieldnames
            matching_rows = []
            
            # Filter rows
            for row in reader:
                if row.get(column) == value:
                    matching_rows.append(row)
                    count += 1
        
        # Write filtered rows to output file
        with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matching_rows)
    
    except (IOError, OSError) as e:
        raise IOError(f"Error processing CSV files: {e}")
    
    return count
