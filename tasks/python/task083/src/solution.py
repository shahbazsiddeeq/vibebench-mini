from __future__ import annotations

import sqlite3


def run_migrations(db_path: str, migrations: list[str]) -> int:
    if not migrations:
        return 0
    conn = sqlite3.connect(db_path)
    conn.isolation_level = None  # manual transaction control
    try:
        conn.execute("BEGIN")
        for sql in migrations:
            try:
                conn.execute(sql)
            except sqlite3.Error as exc:
                conn.execute("ROLLBACK")
                raise RuntimeError(f"migration failed: {sql!r} — {exc}") from exc
        conn.execute("COMMIT")
    finally:
        conn.close()
    return len(migrations)
