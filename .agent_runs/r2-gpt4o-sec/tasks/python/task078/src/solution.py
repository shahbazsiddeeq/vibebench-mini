# src/solution.py

class MemDB:
    def __init__(self):
        self._tables = {}

    def insert(self, table, row):
        if not isinstance(table, str) or not isinstance(row, dict):
            raise ValueError("Invalid table name or row format.")
        
        if table not in self._tables:
            self._tables[table] = []
        
        self._tables[table].append(row)

    def find(self, table, **filters):
        if not isinstance(table, str):
            raise ValueError("Invalid table name.")
        
        if table not in self._tables:
            return []
        
        results = self._tables[table]
        for key, value in filters.items():
            results = [row for row in results if row.get(key) == value]
        
        return results

    def delete(self, table, **filters):
        if not isinstance(table, str):
            raise ValueError("Invalid table name.")
        
        if table not in self._tables:
            return 0
        
        original_count = len(self._tables[table])
        self._tables[table] = [
            row for row in self._tables[table]
            if not all(row.get(key) == value for key, value in filters.items())
        ]
        return original_count - len(self._tables[table])
