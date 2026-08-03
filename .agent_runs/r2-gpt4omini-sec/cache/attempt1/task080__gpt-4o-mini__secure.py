# src/solution.py

import sqlite3
import json
import re
import secrets

def validate_input(rows):
    if not isinstance(rows, list):
        raise ValueError("Rows must be a list.")
    
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("Each row must be a dictionary.")
    
    if not rows:
        return
    
    keys = rows[0].keys()
    for row in rows:
        if row.keys() != keys:
            raise RuntimeError("All rows must have the same keys.")
        
        for key in row.keys():
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                raise ValueError("Invalid column name: {}".format(key))

def batch_insert(db_path, table, rows):
    validate_input(rows)
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            placeholders = ', '.join('?' for _ in rows[0])
            columns = ', '.join(rows[0].keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor.executemany(sql, [tuple(row.values()) for row in rows])
            conn.commit()
            return len(rows)
    except sqlite3.Error as e:
        raise RuntimeError("Database error: {}".format(e)) from e
    except Exception as e:
        raise RuntimeError("An unexpected error occurred: {}".format(e)) from e
