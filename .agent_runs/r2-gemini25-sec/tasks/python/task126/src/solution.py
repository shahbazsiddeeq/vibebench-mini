class Handler:
    """
    Base class for handlers in the Chain of Responsibility pattern.
    """

    def __init__(self):
        self._next_handler = None

    def set_next(self, nxt: 'Handler') -> 'Handler':
        """
        Sets the next handler in the chain.

        Args:
            nxt: The next Handler object.

        Returns:
            The next Handler object, allowing for method chaining.
        """
        if not isinstance(nxt, Handler):
            raise ValueError("Next handler must be an instance of Handler.")
        self._next_handler = nxt
        return nxt

    def handle(self, amount: int) -> str | None:
        """
        Handles the request or passes it to the next handler in the chain.

        Args:
            amount: The integer amount to be handled.

        Returns:
            A string indicating the handling result ('low', 'mid', 'high')
            or None if no handler in the chain can process the amount.

        Raises:
            ValueError: If 'amount' is not an integer.
        """
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if self._next_handler:
            return self._next_handler.handle(amount)
        return None


class LowHandler(Handler):
    """
    Handles amounts less than 100.
    """

    def handle(self, amount: int) -> str | None:
        """
        Handles the request if amount is less than 100, otherwise delegates.
        """
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if amount < 100:
            return 'low'
        return super().handle(amount)


class MidHandler(Handler):
    """
    Handles amounts between 100 and 999 (inclusive).
    """

    def handle(self, amount: int) -> str | None:
        """
        Handles the request if amount is between 100 and 999, otherwise delegates.
        """
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if 100 <= amount < 1000:
            return 'mid'
        return super().handle(amount)


class HighHandler(Handler):
    """
    Handles amounts greater than or equal to 1000.
    """

    def handle(self, amount: int) -> str | None:
        """
        Handles the request if amount is 1000 or more, otherwise delegates.
        """
        if not isinstance(amount, int) or isinstance(amount, bool):
            raise ValueError("Amount must be an integer.")

        if amount >= 1000:
            return 'high'
        return super().handle(amount)
