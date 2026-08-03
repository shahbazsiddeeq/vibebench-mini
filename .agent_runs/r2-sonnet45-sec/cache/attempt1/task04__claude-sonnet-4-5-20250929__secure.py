import csv
from pathlib import Path


def column_mean(path, col):
    """
    Calculate the arithmetic mean of numeric values in a CSV column.
    
    Args:
        path: Path to the CSV file
        col: Name of the column to calculate mean for
    
    Returns:
        float: The arithmetic mean of numeric values in the column
    
    Raises:
        ValueError: If column doesn't exist, is empty, or contains no numeric values
    """
    # Validate inputs
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    if not isinstance(col, str):
        raise ValueError("Column name must be a string")
    
    # Sanitize path - use Path to normalize and validate
    try:
        file_path = Path(path)
        if not file_path.exists():
            raise ValueError(f"File does not exist: {path}")
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {path}")
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid path: {path}") from e
    
    numeric_values = []
    column_found = False
    
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            # Check if column exists in header
            if reader.fieldnames is None:
                raise ValueError("CSV file has no header row")
            
            if col not in reader.fieldnames:
                raise ValueError(f"Column '{col}' not found in CSV header")
            
            column_found = True
            
            # Process each row
            for row in reader:
                value = row.get(col, '')
                
                # Skip empty values
                if not value or not value.strip():
                    continue
                
                # Try to parse as float
                try:
                    numeric_value = float(value.strip())
                    numeric_values.append(numeric_value)
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue
    
    except (OSError, IOError) as e:
        raise ValueError(f"Error reading file: {path}") from e
    except csv.Error as e:
        raise ValueError(f"Error parsing CSV file: {path}") from e
    
    # Check if we found any numeric values
    if not numeric_values:
        if column_found:
            raise ValueError(f"No numeric values found in column '{col}'")
        else:
            raise ValueError(f"Column '{col}' not found or empty")
    
    # Calculate and return mean
    return sum(numeric_values) / len(numeric_values)
