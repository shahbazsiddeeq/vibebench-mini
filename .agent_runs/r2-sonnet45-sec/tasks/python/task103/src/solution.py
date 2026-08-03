class QueryBuilder:
    """
    A secure SQL query builder using parameterized queries.
    Builds SELECT statements with bound parameters to prevent SQL injection.
    """
    
    def __init__(self, table: str):
        """
        Initialize the query builder for a specific table.
        
        Args:
            table: The table name to query from
        """
        if not isinstance(table, str):
            raise TypeError("Table name must be a string")
        if not table or not table.strip():
            raise ValueError("Table name cannot be empty")
        
        # Validate table name contains only safe characters
        # Allow alphanumeric, underscore, and dot (for schema.table)
        if not all(c.isalnum() or c in ('_', '.') for c in table):
            raise ValueError("Table name contains invalid characters")
        
        self._table = table
        self._columns = ["*"]
        self._where_clauses = []
        self._params = []
        self._limit = None
    
    def select(self, *columns: str) -> 'QueryBuilder':
        """
        Set the columns to select.
        
        Args:
            *columns: Column names to select
            
        Returns:
            self for method chaining
        """
        if not columns:
            raise ValueError("At least one column must be specified")
        
        # Validate each column name
        for col in columns:
            if not isinstance(col, str):
                raise TypeError("Column names must be strings")
            if not col or not col.strip():
                raise ValueError("Column name cannot be empty")
            # Allow alphanumeric, underscore, dot, and asterisk
            if not all(c.isalnum() or c in ('_', '.', '*') for c in col):
                raise ValueError(f"Column name '{col}' contains invalid characters")
        
        self._columns = list(columns)
        return self
    
    def where(self, column: str, value) -> 'QueryBuilder':
        """
        Add a WHERE condition with a bound parameter.
        
        Args:
            column: The column name for the condition
            value: The value to bind (will be parameterized)
            
        Returns:
            self for method chaining
        """
        if not isinstance(column, str):
            raise TypeError("Column name must be a string")
        if not column or not column.strip():
            raise ValueError("Column name cannot be empty")
        
        # Validate column name
        if not all(c.isalnum() or c in ('_', '.') for c in column):
            raise ValueError(f"Column name '{column}' contains invalid characters")
        
        self._where_clauses.append(f"{column} = ?")
        self._params.append(value)
        return self
    
    def limit(self, n: int) -> 'QueryBuilder':
        """
        Set a LIMIT clause with a bound parameter.
        
        Args:
            n: The maximum number of rows to return
            
        Returns:
            self for method chaining
        """
        if not isinstance(n, int):
            raise TypeError("Limit must be an integer")
        if n < 0:
            raise ValueError("Limit must be non-negative")
        
        self._limit = n
        return self
    
    def build(self) -> tuple[str, list]:
        """
        Build the final SQL query with bound parameters.
        
        Returns:
            A tuple of (sql_string, parameters_list) where sql_string uses
            '?' placeholders and parameters_list contains the bound values
        """
        # Build SELECT clause
        columns_str = ", ".join(self._columns)
        sql = f"SELECT {columns_str} FROM {self._table}"
        
        # Build WHERE clause
        params = list(self._params)  # Copy the parameters list
        if self._where_clauses:
            where_str = " AND ".join(self._where_clauses)
            sql += f" WHERE {where_str}"
        
        # Build LIMIT clause
        if self._limit is not None:
            sql += " LIMIT ?"
            params.append(self._limit)
        
        return (sql, params)
