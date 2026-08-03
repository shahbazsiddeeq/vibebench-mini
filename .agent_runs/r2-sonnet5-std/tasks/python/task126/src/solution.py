class Handler:
    def __init__(self):
        self._next = None

    def set_next(self, nxt: "Handler") -> "Handler":
        self._next = nxt
        return nxt

    def handle(self, amount: int) -> "str | None":
        if isinstance(amount, bool) or not isinstance(amount, int):
            raise ValueError("amount must be an integer")
        return self._handle(amount)

    def _handle(self, amount: int) -> "str | None":
        if self._next is not None:
            return self._next._handle(amount)
        return None


class LowHandler(Handler):
    def _handle(self, amount: int) -> "str | None":
        if amount < 100:
            return "low"
        return super()._handle(amount)


class MidHandler(Handler):
    def _handle(self, amount: int) -> "str | None":
        if 100 <= amount < 1000:
            return "mid"
        return super()._handle(amount)


class HighHandler(Handler):
    def _handle(self, amount: int) -> "str | None":
        if amount >= 1000:
            return "high"
        return super()._handle(amount)
