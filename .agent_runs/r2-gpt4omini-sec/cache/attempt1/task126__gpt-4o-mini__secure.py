# src/solution.py

class Handler:
    def set_next(self, nxt: 'Handler') -> 'Handler':
        if not isinstance(nxt, Handler):
            raise ValueError("Next handler must be an instance of Handler.")
        self._next_handler = nxt
        return nxt

    def handle(self, amount: int) -> str | None:
        raise NotImplementedError("Subclasses must implement this method.")


class LowHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer.")
        if amount < 100:
            return "low"
        return self._next_handler.handle(amount) if hasattr(self, '_next_handler') else None


class MidHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer.")
        if 100 <= amount < 1000:
            return "mid"
        return self._next_handler.handle(amount) if hasattr(self, '_next_handler') else None


class HighHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer.")
        if amount >= 1000:
            return "high"
        return self._next_handler.handle(amount) if hasattr(self, '_next_handler') else None
