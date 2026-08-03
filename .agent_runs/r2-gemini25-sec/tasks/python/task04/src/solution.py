import csv
import os

def column_mean(path: str, col: str) -> float:
    """
    Calculates the arithmetic mean of numeric values in a specified column of a CSV file.

    Args:
        path: The path to the CSV file.
        col: The name of the column to calculate the mean for.

    Returns:
        The arithmetic mean of the numeric values in the specified column.

    Raises:
        ValueError: If the file does not exist, is not a regular file,
                    the column is not found, or no numeric values are
                    found in the column.
        IOError: If there's an issue reading the file.
    """
    if not isinstance(path, str) or not path:
        raise ValueError("CSV file path must be a non-empty string.")
    if not isinstance(col, str) or not col:
        raise ValueError("Column name must be a non-empty string.")

    if not os.path.exists(path):
        raise ValueError(f"File not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a regular file: {path}")

    total_sum = 0.0
    count = 0

    try:
        with open(path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)

            try:
                header = next(reader)
            except StopIteration:
                # File is empty or only contains header, but no data rows
                raise ValueError(f"CSV file '{path}' is empty or contains no data rows.")

            try:
                col_index = header.index(col)
            except ValueError:
                raise ValueError(f"Column '{col}' not found in the CSV header: {header}")

            for row_num, row in enumerate(reader, start=2): # Start counting rows from 2 (1 for header, 1 for first data row)
                if col_index < len(row):
                    value_str = row[col_index].strip()
                    if value_str: # Only attempt conversion if the string is not empty
                        try:
                            total_sum += float(value_str)
                            count += 1
                        except ValueError:
                            # Skip non-numeric values
                            pass
                # If col_index is out of bounds for a specific row, it means the row is malformed
                # and we effectively treat that column's value as non-existent/non-numeric for that row.

    except FileNotFoundError: # Redundant due to os.path.exists check, but good for robustness
        raise ValueError(f"File not found: {path}")
    except IOError as e:
        raise IOError(f"Error reading CSV file '{path}': {e}")
    except Exception as e:
        # Catch any other unexpected errors during CSV parsing
        raise ValueError(f"An unexpected error occurred while processing '{path}': {e}")

    if count == 0:
        raise ValueError(f"No numeric values found in column '{col}' in file '{path}'.")

    return total_sum / count
