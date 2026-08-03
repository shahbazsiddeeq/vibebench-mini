import csv


def dedupe_csv(in_path, out_path, key):
    with open(in_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames or key not in fieldnames:
            raise KeyError(key)

        rows = list(reader)

    last_index = {}
    for idx, row in enumerate(rows):
        last_index[row[key]] = idx

    kept_indices = sorted(last_index.values())
    result_rows = [rows[i] for i in kept_indices]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_rows:
            writer.writerow(row)

    return len(result_rows)
