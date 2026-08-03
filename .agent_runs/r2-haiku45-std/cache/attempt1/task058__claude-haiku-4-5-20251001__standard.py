import csv


def csv_filter(in_path, out_path, column, value):
    """
    Filter CSV rows by column value and write matching rows to output file.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        column: Column name to filter by
        value: Value to match in the column
        
    Returns:
        Count of data rows written (excluding header)
        
    Raises:
        KeyError: If column not found in header
    """
    count = 0
    
    with open(in_path, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        
        # Check if column exists in header
        if reader.fieldnames is None or column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in header")
        
        fieldnames = reader.fieldnames
        
        with open(out_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                if row[column] == value:
                    writer.writerow(row)
                    count += 1
    
    return count
