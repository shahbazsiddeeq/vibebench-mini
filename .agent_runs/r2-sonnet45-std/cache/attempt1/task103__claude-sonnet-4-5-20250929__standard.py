class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self.columns = ["*"]
        self.conditions = []
        self.params = []
        self.limit_value = None
    
    def select(self, *columns):
        if columns:
            self.columns = list(columns)
        return self
    
    def where(self, column, value):
        self.conditions.append(f"{column} = ?")
        self.params.append(value)
        return self
    
    def limit(self, n):
        self.limit_value = n
        return self
    
    def build(self):
        # Build SELECT clause
        columns_str = ", ".join(self.columns)
        sql = f"SELECT {columns_str} FROM {self.table}"
        
        # Build WHERE clause
        if self.conditions:
            where_clause = " AND ".join(self.conditions)
            sql += f" WHERE {where_clause}"
        
        # Build params list
        params = self.params.copy()
        
        # Add LIMIT clause
        if self.limit_value is not None:
            sql += " LIMIT ?"
            params.append(self.limit_value)
        
        return (sql, params)
