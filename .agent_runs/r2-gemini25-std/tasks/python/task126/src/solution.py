class Handler:
    def __init__(self):
        self._next_handler = None

    def set_next(self, nxt: 'Handler') -> 'Handler':
        self._next_handler = nxt
        return nxt

    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")
        
        if self._next_handler:
            return self._next_handler.handle(amount)
        return None


class LowHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if amount < 100:
            return 'low'
        else:
            return super().handle(amount)


class MidHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if 100 <= amount < 1000:
            return 'mid'
        else:
            return super().handle(amount)


class HighHandler(Handler):
    def handle(self, amount: int) -> str | None:
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if amount >= 1000:
            return 'high'
        else:
            return super().handle(amount)
