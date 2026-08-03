# src/solution.py

class Handler:
    def set_next(self, nxt: 'Handler') -> 'Handler':
        self._next = nxt
        return nxt

    def handle(self, amount: int) -> str | None:
        raise NotImplementedError("Must be implemented by subclasses")


class LowHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer")
        if amount < 100:
            return "low"
        return super().handle(amount)


class MidHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer")
        if 100 <= amount < 1000:
            return "mid"
        return super().handle(amount)


class HighHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer")
        if amount >= 1000:
            return "high"
        return super().handle(amount)
