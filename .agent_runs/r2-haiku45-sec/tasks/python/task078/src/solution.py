"""
In-Memory Database implementation with insert, find, and delete operations.
"""


class MemDB:
    """A simple in-memory database supporting multiple tables."""
    
    def __init__(self):
        """Initialize the database with an empty dictionary of tables."""
        self._tables = {}
    
    def insert(self, table, row):
        """
        Insert a row into a table.
        
        Args:
            table: The name of the table (string)
            row: A dictionary representing the row to insert
            
        Raises:
            TypeError: If table is not a string or row is not a dict
            ValueError: If row is empty
        """
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        if not isinstance(row, dict):
            raise TypeError("Row must be a dictionary")
        if not row:
            raise ValueError("Row cannot be empty")
        
        # Create table if it doesn't exist
        if table not in self._tables:
            self._tables[table] = []
        
        # Insert a copy of the row to prevent external modifications
        self._tables[table].append(dict(row))
    
    def find(self, table, **filters):
        """
        Find rows in a table matching all filter conditions (AND logic).
        
        Args:
            table: The name of the table (string)
            **filters: Keyword arguments representing filter conditions
            
        Returns:
            A list of dictionaries matching all filter conditions.
            Returns empty list if table doesn't exist or no matches found.
            
        Raises:
            TypeError: If table is not a string
        """
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        
        # Return empty list if table doesn't exist
        if table not in self._tables:
            return []
        
        rows = self._tables[table]
        
        # If no filters, return all rows (as copies)
        if not filters:
            return [dict(row) for row in rows]
        
        # Filter rows: all filter conditions must match (AND logic)
        result = []
        for row in rows:
            if all(row.get(key) == value for key, value in filters.items()):
                result.append(dict(row))
        
        return result
    
    def delete(self, table, **filters):
        """
        Delete rows from a table matching all filter conditions (AND logic).
        
        Args:
            table: The name of the table (string)
            **filters: Keyword arguments representing filter conditions
            
        Returns:
            The number of rows deleted.
            
        Raises:
            TypeError: If table is not a string
        """
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        
        # Return 0 if table doesn't exist
        if table not in self._tables:
            return 0
        
        rows = self._tables[table]
        
        # If no filters, delete all rows
        if not filters:
            count = len(rows)
            self._tables[table] = []
            return count
        
        # Count and remove rows matching all filter conditions
        initial_count = len(rows)
        self._tables[table] = [
            row for row in rows
            if not all(row.get(key) == value for key, value in filters.items())
        ]
        deleted_count = initial_count - len(self._tables[table])
        
        return deleted_count
