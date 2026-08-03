"""
QueryBuilder module for constructing parameterized SQL SELECT statements.
Uses the builder pattern with a fluent interface.
"""


class QueryBuilder:
    """
    Builds parameterized SQL SELECT statements using a fluent interface.
    All user-supplied values are bound as parameters, never interpolated into SQL.
    """

    def __init__(self, table: str) -> None:
        """
        Initialize QueryBuilder with a table name.
        
        Args:
            table: The table name to query from (validated as identifier)
        
        Raises:
            ValueError: If table name is invalid
        """
        if not isinstance(table, str):
            raise ValueError("Table name must be a string")
        if not table:
            raise ValueError("Table name cannot be empty")
        if not self._is_valid_identifier(table):
            raise ValueError("Invalid table name")
        
        self._table = table
        self._columns = ["*"]
        self._where_conditions = []
        self._params = []
        self._limit_value = None

    @staticmethod
    def _is_valid_identifier(name: str) -> bool:
        """
        Validate that a name is a valid SQL identifier.
        Allows alphanumeric characters, underscores, and dots (for schema.table).
        
        Args:
            name: The identifier to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not name:
            return False
        # Allow alphanumeric, underscore, and dot for schema.table notation
        return all(c.isalnum() or c in ('_', '.') for c in name)

    def select(self, *columns: str) -> "QueryBuilder":
        """
        Set the columns to select.
        
        Args:
            *columns: Column names to select
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If no columns provided or invalid column names
        """
        if not columns:
            raise ValueError("At least one column must be specified")
        
        for col in columns:
            if not isinstance(col, str):
                raise ValueError("Column names must be strings")
            if not col:
                raise ValueError("Column name cannot be empty")
            if not self._is_valid_identifier(col):
                raise ValueError(f"Invalid column name: {col}")
        
        self._columns = list(columns)
        return self

    def where(self, column: str, value) -> "QueryBuilder":
        """
        Add an equality condition to the WHERE clause.
        
        Args:
            column: The column name to filter on
            value: The value to compare (will be bound as parameter)
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If column name is invalid
        """
        if not isinstance(column, str):
            raise ValueError("Column name must be a string")
        if not column:
            raise ValueError("Column name cannot be empty")
        if not self._is_valid_identifier(column):
            raise ValueError(f"Invalid column name: {column}")
        
        self._where_conditions.append(column)
        self._params.append(value)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        """
        Set the LIMIT clause.
        
        Args:
            n: The maximum number of rows to return
            
        Returns:
            self for method chaining
            
        Raises:
            ValueError: If n is not a positive integer
        """
        if not isinstance(n, int):
            raise ValueError("Limit must be an integer")
        if n <= 0:
            raise ValueError("Limit must be positive")
        
        self._limit_value = n
        return self

    def build(self) -> tuple[str, list]:
        """
        Build the SQL statement and return it with parameters.
        
        Returns:
            A tuple of (sql_string, params_list) where sql_string contains
            "?" placeholders for all bound values and params_list contains
            those values in order.
        """
        # Build SELECT clause
        sql_parts = [f"SELECT {', '.join(self._columns)} FROM {self._table}"]
        
        # Build WHERE clause if conditions exist
        if self._where_conditions:
            where_clauses = [f"{col} = ?" for col in self._where_conditions]
            sql_parts.append(f"WHERE {' AND '.join(where_clauses)}")
        
        # Build LIMIT clause if set
        if self._limit_value is not None:
            sql_parts.append("LIMIT ?")
            # Add limit value to params
            params = self._params + [self._limit_value]
        else:
            params = self._params[:]
        
        sql = " ".join(sql_parts)
        return (sql, params)
