# src/solution.py

class MemDB:
    def __init__(self):
        self.tables = {}

    def _validate_table(self, table):
        if not isinstance(table, str) or not table.isidentifier():
            raise ValueError("Invalid table name.")

    def _validate_row(self, row):
        if not isinstance(row, dict):
            raise ValueError("Row must be a dictionary.")

    def insert(self, table, row):
        self._validate_table(table)
        self._validate_row(row)

        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(row)

    def find(self, table, **filters):
        self._validate_table(table)

        if table not in self.tables:
            return []

        results = self.tables[table]
        for key, value in filters.items():
            results = [row for row in results if row.get(key) == value]
        return results

    def delete(self, table, **filters):
        self._validate_table(table)

        if table not in self.tables:
            return 0

        original_count = len(self.tables[table])
        self.tables[table] = [row for row in self.tables[table] if not all(row.get(k) == v for k, v in filters.items())]
        return original_count - len(self.tables[table])
