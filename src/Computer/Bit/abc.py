import abc
import enum
from typing import TypeVar

E = TypeVar("E", bound=enum.Enum)
# This is to represent an arbitrary enumeration type.

class IBit(metaclass=abc.ABCMeta):
    
    """
    This implements a single bit to be passed around.
    """

    @abc.abstractclassmethod
    def __init__(self, value: E):
        ...


class IBitString(metaclass=abc.ABCMeta):

    """
    This implements a deque data structure holding `Bit` instances.
    """

    @abc.abstractclassmethod
    def __init__(self, max_length: int):
        """Constructor..."""
        ...

    @abc.abstractclassmethod
    def pop_left(self) -> IBit:
        """Pop off the left-most bit."""

        ...

    @abc.abstractclassmethod
    def pop_right(self) -> IBit:
        """Pop off the right-most bit."""

        ...

    @abc.abstractclassmethod
    def push_left(self) -> IBit:
        """Push a bit to the left side of the deque."""

        ...

    @abc.abstractclassmethod
    def push_right(self) -> IBit:
        """Push a bit to the right side of the deque."""

        ...