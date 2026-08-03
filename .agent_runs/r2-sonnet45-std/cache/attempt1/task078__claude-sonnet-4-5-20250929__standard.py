class MemDB:
    def __init__(self):
        self.tables = {}
    
    def insert(self, table, row):
        """Insert a row (dict) into the specified table."""
        if table not in self.tables:
            self.tables[table] = []
        self.tables[table].append(row.copy())
    
    def find(self, table, **filters):
        """Find all rows in table matching all filters (AND logic)."""
        if table not in self.tables:
            return []
        
        result = []
        for row in self.tables[table]:
            # Check if row matches all filters
            matches = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    matches = False
                    break
            if matches:
                result.append(row.copy())
        
        return result
    
    def delete(self, table, **filters):
        """Delete all rows matching filters and return count deleted."""
        if table not in self.tables:
            return 0
        
        rows_to_keep = []
        deleted_count = 0
        
        for row in self.tables[table]:
            # Check if row matches all filters
            matches = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    matches = False
                    break
            
            if matches:
                deleted_count += 1
            else:
                rows_to_keep.append(row)
        
        self.tables[table] = rows_to_keep
        return deleted_count
