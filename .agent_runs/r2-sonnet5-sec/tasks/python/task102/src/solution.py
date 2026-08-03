"""
Observer Pattern implementation.

This module provides a minimal, secure, and self-contained implementation of
the classic Observer design pattern.

Classes
-------
Observer
    Abstract base class defining the interface observers must implement.
Subject
    Maintains a set of observers and notifies them of events.

Security considerations
------------------------
- No use of eval/exec or dynamic code execution.
- No external I/O; the module only manipulates in-memory data structures.
- Input validation is performed on public methods to guard against misuse
  (e.g., attaching non-Observer objects, invalid event types).
- Errors are raised using standard exceptions with generic messages that do
  not leak internal state or stack details.
"""

from __future__ import annotations

from typing import Any, List, Optional


class Observer:
    """Abstract base class for observers.

    Subclasses must override :meth:`update` to handle notifications.
    """

    def update(self, event: str, data: Optional[Any] = None) -> None:
        """Handle a notification event.

        Parameters
        ----------
        event : str
            The name/type of the event.
        data : Any, optional
            Additional data associated with the event.

        Notes
        -----
        The base implementation does nothing; subclasses should override
        this method to provide custom behavior.
        """
        # Default no-op implementation.
        return None


class Subject:
    """Subject that maintains a list of observers and notifies them.

    Each ``Subject`` instance keeps its own independent list of observers,
    ensuring that notifications sent from one subject do not affect
    observers attached only to a different subject.
    """

    def __init__(self) -> None:
        # Use a list to preserve attachment order while avoiding duplicate
        # entries via explicit checks in attach().
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer to this subject.

        Parameters
        ----------
        observer : Observer
            The observer instance to attach. Must be an instance of
            :class:`Observer`.

        Raises
        ------
        TypeError
            If ``observer`` is not an instance of :class:`Observer`.
        """
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an instance of Observer")

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from this subject.

        If the observer is not currently attached, this is a no-op and
        does not raise an error, to keep the API forgiving and simple.

        Parameters
        ----------
        observer : Observer
            The observer instance to detach.
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            # Observer wasn't attached; silently ignore.
            pass

    def notify(self, event: str, data: Optional[Any] = None) -> None:
        """Notify all attached observers of an event.

        Parameters
        ----------
        event : str
            The name/type of the event. Must be a string.
        data : Any, optional
            Additional data to pass along with the event.

        Raises
        ------
        TypeError
            If ``event`` is not a string.
        """
        if not isinstance(event, str):
            raise TypeError("event must be a string")

        # Iterate over a shallow copy to guard against mutation of the
        # observer list during iteration (e.g., an observer detaching
        # itself or another observer inside its update() method).
        for observer in list(self._observers):
            observer.update(event, data)
