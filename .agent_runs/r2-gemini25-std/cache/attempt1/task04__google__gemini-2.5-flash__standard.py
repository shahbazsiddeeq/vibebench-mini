import csv

def column_mean(path, col):
    """
    Calculates the arithmetic mean of numeric values in a specified column of a CSV file.

    Args:
        path (str): The path to the CSV file.
        col (str): The name of the column for which to calculate the mean.

    Returns:
        float: The arithmetic mean of the numeric values in the column.

    Raises:
        ValueError: If no numeric values are found in the column (e.g., column is empty,
                    absent from the header, or contains only non-numeric values).
    """
    total_sum = 0.0
    count = 0

    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        try:
            header = next(reader)
        except StopIteration:
            # File is empty or only contains header, no data rows
            raise ValueError("No numeric values found in the column.")

        try:
            col_index = header.index(col)
        except ValueError:
            raise ValueError(f"Column '{col}' not found in the CSV header.")

        for row in reader:
            if len(row) > col_index:  # Ensure the row has enough columns
                value_str = row[col_index].strip()
                try:
                    value = float(value_str)
                    total_sum += value
                    count += 1
                except ValueError:
                    # Skip non-numeric values
                    pass

    if count == 0:
        raise ValueError("No numeric values found in the column.")
    
    return total_sum / count
