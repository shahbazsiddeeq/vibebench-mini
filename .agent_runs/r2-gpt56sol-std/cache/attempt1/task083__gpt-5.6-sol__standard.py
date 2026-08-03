import sqlite3
from os import PathLike
from typing import Iterable, Union


def run_migrations(
    db_path: Union[str, bytes, PathLike[str], PathLike[bytes]],
    migrations: Iterable[str],
) -> int:
    """Execute all migration statements atomically and return their count."""
    connection = sqlite3.connect(db_path)
    count = 0

    try:
        connection.execute("BEGIN")

        for statement in migrations:
            try:
                connection.execute(statement)
            except Exception as exc:
                connection.rollback()
                raise RuntimeError(
                    f"Migration failed for statement {statement!r}: {exc}"
                ) from exc
            count += 1

        connection.commit()
        return count
    except RuntimeError:
        raise
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
