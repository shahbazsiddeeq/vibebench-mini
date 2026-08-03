import csv


def column_mean(path, col):
    """
    Returns the arithmetic mean of numeric values in column `col` of a CSV file.
    
    Args:
        path: Path to the CSV file
        col: Column name to calculate mean for
        
    Returns:
        float: The arithmetic mean of numeric values in the column
        
    Raises:
        ValueError: If column is missing, empty, or contains only non-numeric values
    """
    numeric_values = []
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if column exists in header
        if reader.fieldnames is None or col not in reader.fieldnames:
            raise ValueError(f"Column '{col}' not found in CSV header")
        
        # Iterate through rows and collect numeric values
        for row in reader:
            value = row[col]
            try:
                numeric_values.append(float(value))
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
    
    # Raise error if no numeric values found
    if not numeric_values:
        raise ValueError(f"No numeric values found in column '{col}'")
    
    # Calculate and return mean
    return sum(numeric_values) / len(numeric_values)
