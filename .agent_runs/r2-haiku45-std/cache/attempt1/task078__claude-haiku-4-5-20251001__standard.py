class MemDB:
    def __init__(self):
        self.tables = {}
    
    def insert(self, table, row):
        """Insert a row into a table."""
        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(row.copy())
    
    def find(self, table, **filters):
        """Find rows in a table matching all filters (AND logic)."""
        if table not in self.tables:
            return []
        
        results = []
        for row in self.tables[table]:
            # Check if row matches all filters
            if all(row.get(key) == value for key, value in filters.items()):
                results.append(row.copy())
        
        return results
    
    def delete(self, table, **filters):
        """Delete rows matching all filters and return count of deleted rows."""
        if table not in self.tables:
            return 0
        
        original_count = len(self.tables[table])
        
        # Keep only rows that don't match all filters
        self.tables[table] = [
            row for row in self.tables[table]
            if not all(row.get(key) == value for key, value in filters.items())
        ]
        
        deleted_count = original_count - len(self.tables[table])
        return deleted_count
