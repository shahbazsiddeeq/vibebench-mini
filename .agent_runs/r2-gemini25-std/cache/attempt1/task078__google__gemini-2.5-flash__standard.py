class MemDB:
    def __init__(self):
        self._data = {}

    def insert(self, table: str, row: dict):
        if table not in self._data:
            self._data[table] = []
        self._data[table].append(row)

    def find(self, table: str, **filters) -> list[dict]:
        if table not in self._data:
            return []

        results = []
        for row in self._data[table]:
            match = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    match = False
                    break
            if match:
                results.append(row)
        return results

    def delete(self, table: str, **filters) -> int:
        if table not in self._data:
            return 0

        initial_count = len(self._data[table])
        
        # Create a new list for rows that do not match the filters
        # This avoids issues with modifying a list while iterating over it
        new_table_data = []
        deleted_count = 0

        for row in self._data[table]:
            match = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    match = False
                    break
            
            if not match:
                new_table_data.append(row)
            else:
                deleted_count += 1
        
        self._data[table] = new_table_data
        return deleted_count
