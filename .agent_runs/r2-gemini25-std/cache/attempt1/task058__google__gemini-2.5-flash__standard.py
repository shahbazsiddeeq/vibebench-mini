import csv


def csv_filter(in_path, out_path, column, value):
    """
    Filters a CSV file based on a column's value and writes the matching rows
    to a new CSV file.

    Args:
        in_path (str): The path to the input CSV file.
        out_path (str): The path to the output CSV file.
        column (str): The name of the column to filter by.
        value (str): The value to match in the specified column.

    Returns:
        int: The count of data rows written to the output file.

    Raises:
        KeyError: If the specified column is not found in the CSV header.
    """
    written_rows_count = 0

    with open(in_path, "r", newline="") as infile:
        reader = csv.DictReader(infile)

        if column not in reader.fieldnames:
            raise KeyError(f"Column '{column}' not found in the CSV header.")

        with open(out_path, "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                if row.get(column) == value:
                    writer.writerow(row)
                    written_rows_count += 1

    return written_rows_count
