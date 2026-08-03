import csv


def column_mean(path, col):
    """
    Returns the arithmetic mean of the numeric values in column `col` of a CSV file.
    
    Args:
        path: Path to the CSV file with a header row
        col: Name of the column to calculate mean for
    
    Returns:
        float: The arithmetic mean of numeric values in the column
    
    Raises:
        ValueError: If the column is absent, empty, or contains only non-numeric values
    """
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if column exists in header
        if col not in reader.fieldnames:
            raise ValueError(f"Column '{col}' not found in CSV header")
        
        numeric_values = []
        
        for row in reader:
            value = row[col]
            try:
                numeric_value = float(value)
                numeric_values.append(numeric_value)
            except (ValueError, TypeError):
                # Skip non-numeric values
                continue
        
        # If no numeric values were found, raise ValueError
        if not numeric_values:
            raise ValueError(f"No numeric values found in column '{col}'")
        
        return sum(numeric_values) / len(numeric_values)
