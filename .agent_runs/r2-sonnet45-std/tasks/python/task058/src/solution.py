import csv


def csv_filter(in_path, out_path, column, value):
    """
    Filters a CSV file by column value.
    
    Args:
        in_path: Path to input CSV file
        out_path: Path to output CSV file
        column: Column name to filter on
        value: Value to match in the column
    
    Returns:
        Count of data rows written (excluding header)
    
    Raises:
        KeyError: If column is not in the CSV header
    """
    with open(in_path, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        
        # Check if column exists in header
        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in CSV header")
        
        # Read and filter rows
        filtered_rows = []
        for row in reader:
            if row[column] == value:
                filtered_rows.append(row)
        
        # Write filtered rows to output file
        with open(out_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
        
        return len(filtered_rows)
