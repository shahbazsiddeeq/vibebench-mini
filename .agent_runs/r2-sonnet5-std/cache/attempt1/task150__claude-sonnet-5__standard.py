import os


def rotate_log(path: str, message: str, max_bytes: int, backup_count: int) -> None:
    if max_bytes < 1 or backup_count < 0:
        raise ValueError("max_bytes must be >= 1 and backup_count must be >= 0")

    line_bytes = message.encode('utf-8') + b'\n'
    line_size = len(line_bytes)

    if os.path.exists(path):
        current_size = os.path.getsize(path)
    else:
        current_size = 0

    if current_size > 0 and current_size + line_size > max_bytes:
        if backup_count == 0:
            with open(path, 'wb') as f:
                pass
        else:
            last_backup = path + '.' + str(backup_count)
            if os.path.exists(last_backup):
                os.remove(last_backup)
            for i in range(backup_count - 1, 0, -1):
                src = path + '.' + str(i)
                dst = path + '.' + str(i + 1)
                if os.path.exists(src):
                    os.rename(src, dst)
            os.rename(path, path + '.1')

    with open(path, 'ab') as f:
        f.write(line_bytes)
