import csv
from pathlib import Path


def column_mean(path: str, col: str) -> float:
    """
    Calculate the arithmetic mean of numeric values in a CSV column.
    
    Args:
        path: Path to the CSV file
        col: Column name to calculate mean for
        
    Returns:
        The arithmetic mean of numeric values in the column
        
    Raises:
        ValueError: If column is missing, empty, or contains no numeric values
        FileNotFoundError: If the file does not exist
    """
    # Validate inputs
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(col, str):
        raise TypeError("col must be a string")
    
    # Check file exists and is readable
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    numeric_values = []
    column_found = False
    
    try:
        with open(path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            # Check if DictReader was able to parse headers
            if reader.fieldnames is None:
                raise ValueError("CSV file has no header row")
            
            # Check if column exists in header
            if col not in reader.fieldnames:
                raise ValueError(f"Column '{col}' not found in CSV header")
            
            column_found = True
            
            # Process each row
            for row in reader:
                if row is None:
                    continue
                    
                value = row.get(col)
                
                # Skip empty values
                if value is None or value == '':
                    continue
                
                # Try to parse as float
                try:
                    numeric_value = float(value)
                    numeric_values.append(numeric_value)
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue
    
    except (FileNotFoundError, IsADirectoryError) as e:
        raise FileNotFoundError(f"Cannot read file: {path}") from e
    except csv.Error as e:
        raise ValueError(f"Invalid CSV format: {e}") from e
    
    # Check if we found any numeric values
    if not numeric_values:
        raise ValueError(f"No numeric values found in column '{col}'")
    
    # Calculate and return mean
    return sum(numeric_values) / len(numeric_values)
