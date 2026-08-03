import csv
import os
from pathlib import Path


def csv_filter(in_path, out_path, column, value):
    """
    Filters CSV rows where the specified column matches the given value.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        column: Column name to filter on
        value: Value to match in the specified column
        
    Returns:
        Count of data rows written (excluding header)
        
    Raises:
        KeyError: If column is not in the CSV header
        FileNotFoundError: If input file doesn't exist
        PermissionError: If file permissions prevent reading/writing
    """
    # Validate input path
    if not isinstance(in_path, (str, Path)):
        raise TypeError("in_path must be a string or Path")
    if not isinstance(out_path, (str, Path)):
        raise TypeError("out_path must be a string or Path")
    if not isinstance(column, str):
        raise TypeError("column must be a string")
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    
    # Convert to string paths
    in_path = str(in_path)
    out_path = str(out_path)
    
    # Validate that input file exists
    if not os.path.exists(in_path):
        raise FileNotFoundError(f"Input file not found: {in_path}")
    
    # Validate that input is a file
    if not os.path.isfile(in_path):
        raise ValueError(f"Input path is not a file: {in_path}")
    
    count = 0
    
    try:
        with open(in_path, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Check if column exists in header
            if reader.fieldnames is None:
                raise ValueError("Input CSV file is empty or has no header")
            
            if column not in reader.fieldnames:
                raise KeyError(f"Column '{column}' not found in CSV header")
            
            # Prepare output file
            with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                
                # Filter and write matching rows
                for row in reader:
                    if row.get(column) == value:
                        writer.writerow(row)
                        count += 1
    
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(in_path, 'r', newline='', encoding='latin-1') as infile:
                reader = csv.DictReader(infile)
                
                if reader.fieldnames is None:
                    raise ValueError("Input CSV file is empty or has no header")
                
                if column not in reader.fieldnames:
                    raise KeyError(f"Column '{column}' not found in CSV header")
                
                with open(out_path, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    
                    for row in reader:
                        if row.get(column) == value:
                            writer.writerow(row)
                            count += 1
        except Exception:
            raise
    
    return count
