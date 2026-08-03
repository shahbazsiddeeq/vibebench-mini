import threading


class RWLock:
    """A thread-safe, writer-preferring read-write lock."""

    def __init__(self) -> None:
        self._condition = threading.Condition(threading.Lock())
        self._active_readers = 0
        self._reader_holds: dict[threading.Thread, int] = {}
        self._writer: threading.Thread | None = None
        self._waiting_writers = 0

    @property
    def active_readers(self) -> int:
        with self._condition:
            return self._active_readers

    def acquire_read(self) -> None:
        thread = threading.current_thread()

        with self._condition:
            while self._writer is not None or (
                self._waiting_writers > 0 and thread not in self._reader_holds
            ):
                self._condition.wait()

            self._active_readers += 1
            self._reader_holds[thread] = self._reader_holds.get(thread, 0) + 1

    def release_read(self) -> None:
        thread = threading.current_thread()

        with self._condition:
            held = self._reader_holds.get(thread, 0)
            if held == 0:
                raise ValueError("cannot release an unheld read lock")

            if held == 1:
                del self._reader_holds[thread]
            else:
                self._reader_holds[thread] = held - 1

            self._active_readers -= 1
            if self._active_readers == 0:
                self._condition.notify_all()

    def acquire_write(self) -> None:
        thread = threading.current_thread()

        with self._condition:
            self._waiting_writers += 1
            try:
                while self._writer is not None or self._active_readers > 0:
                    self._condition.wait()
            except BaseException:
                self._waiting_writers -= 1
                self._condition.notify_all()
                raise

            self._waiting_writers -= 1
            self._writer = thread

    def release_write(self) -> None:
        thread = threading.current_thread()

        with self._condition:
            if self._writer is not thread:
                raise ValueError("cannot release an unheld write lock")

            self._writer = None
            self._condition.notify_all()
