import csv


def csv_filter(in_path, out_path, column, value):
    with open(in_path, newline="") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        if fieldnames is None or column not in fieldnames:
            raise KeyError(column)

        count = 0
        with open(out_path, "w", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get(column) == value:
                    writer.writerow(row)
                    count += 1

    return count
