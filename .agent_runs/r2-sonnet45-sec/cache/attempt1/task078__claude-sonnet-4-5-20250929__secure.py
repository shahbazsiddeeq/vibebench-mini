class MemDB:
    """In-memory database with insert, find, and delete operations."""
    
    def __init__(self):
        """Initialize an empty database."""
        self._tables = {}
    
    def insert(self, table, row):
        """
        Insert a row into a table.
        
        Args:
            table: Table name (string)
            row: Dictionary representing the row to insert
        
        Raises:
            TypeError: If table is not a string or row is not a dict
            ValueError: If table name or row keys contain invalid characters
        """
        # Validate inputs
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        if not isinstance(row, dict):
            raise TypeError("Row must be a dictionary")
        
        # Validate table name (prevent injection-like attacks)
        if not table or not table.strip():
            raise ValueError("Table name cannot be empty")
        
        # Validate row keys are strings
        for key in row.keys():
            if not isinstance(key, str):
                raise TypeError("Row keys must be strings")
        
        # Create table if it doesn't exist
        if table not in self._tables:
            self._tables[table] = []
        
        # Insert a copy of the row to prevent external modifications
        self._tables[table].append(dict(row))
    
    def find(self, table, **filters):
        """
        Find rows in a table matching all filters (AND operation).
        
        Args:
            table: Table name (string)
            **filters: Key-value pairs to filter by
        
        Returns:
            List of dictionaries representing matching rows (copies)
        
        Raises:
            TypeError: If table is not a string
        """
        # Validate inputs
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        
        # Return empty list if table doesn't exist
        if table not in self._tables:
            return []
        
        # Validate filter keys are strings
        for key in filters.keys():
            if not isinstance(key, str):
                raise TypeError("Filter keys must be strings")
        
        results = []
        
        # Iterate through all rows in the table
        for row in self._tables[table]:
            # Check if row matches all filters
            match = True
            for key, value in filters.items():
                # If key doesn't exist in row or value doesn't match, skip this row
                if key not in row or row[key] != value:
                    match = False
                    break
            
            if match:
                # Return a copy to prevent external modifications
                results.append(dict(row))
        
        return results
    
    def delete(self, table, **filters):
        """
        Delete rows from a table matching all filters (AND operation).
        
        Args:
            table: Table name (string)
            **filters: Key-value pairs to filter by
        
        Returns:
            Number of rows deleted (integer)
        
        Raises:
            TypeError: If table is not a string
        """
        # Validate inputs
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        
        # Return 0 if table doesn't exist
        if table not in self._tables:
            return 0
        
        # Validate filter keys are strings
        for key in filters.keys():
            if not isinstance(key, str):
                raise TypeError("Filter keys must be strings")
        
        # Find rows to keep (those that don't match the filters)
        rows_to_keep = []
        deleted_count = 0
        
        for row in self._tables[table]:
            # Check if row matches all filters
            match = True
            for key, value in filters.items():
                if key not in row or row[key] != value:
                    match = False
                    break
            
            if match:
                # This row should be deleted
                deleted_count += 1
            else:
                # Keep this row
                rows_to_keep.append(row)
        
        # Update the table with only the rows to keep
        self._tables[table] = rows_to_keep
        
        return deleted_count
