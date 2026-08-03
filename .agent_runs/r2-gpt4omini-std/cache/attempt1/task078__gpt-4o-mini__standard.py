# src/solution.py

class MemDB:
    def __init__(self):
        self.tables = {}

    def insert(self, table: str, row: dict) -> None:
        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(row)

    def find(self, table: str, **filters) -> list[dict]:
        if table not in self.tables:
            return []
        results = self.tables[table]
        for key, value in filters.items():
            results = [row for row in results if row.get(key) == value]
        return results

    def delete(self, table: str, **filters) -> int:
        if table not in self.tables:
            return 0
        original_count = len(self.tables[table])
        self.tables[table] = [row for row in self.tables[table] if not all(row.get(key) == value for key, value in filters.items())]
        return original_count - len(self.tables[table])
