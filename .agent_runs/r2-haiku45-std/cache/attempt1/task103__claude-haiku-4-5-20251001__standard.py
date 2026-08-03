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
    
    def where(self, column: str, value):
        self.conditions.append(column)
        self.params.append(value)
        return self
    
    def limit(self, n: int):
        self.limit_value = n
        return self
    
    def build(self) -> tuple[str, list]:
        # Build SELECT clause
        sql = f"SELECT {', '.join(self.columns)} FROM {self.table}"
        
        # Build WHERE clause
        if self.conditions:
            where_clauses = [f"{col} = ?" for col in self.conditions]
            sql += " WHERE " + " AND ".join(where_clauses)
        
        # Build LIMIT clause
        if self.limit_value is not None:
            sql += " LIMIT ?"
            params = self.params + [self.limit_value]
        else:
            params = self.params
        
        return (sql, params)
