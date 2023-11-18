from typing import List

from .bit import Bit, BitError
from Computer.Bit.abc import IBitString


class BitString(IBitString):

    """
    This will implement a string of bits. This will make it easier to manipulate and
    work with multiple bits going forward.

    Attributes:
        max_length: the maximum number of bits this can hold (private)
        bits:       the collection of bits (private)
    """

    def __init__(self, max_length: int):
        """
        Constructor...

        Args:
            max_length:
                The maximum number of bits this can hold.
        """

        self._max_length: int = max_length
        """
        The maximum number of bits this can hold.

        Type:
            int
        """

        self._bits: List[Bit] = []
        """
        The collection of bits.

        Type:
            List[Bit]
        """

    def __iter__(self) -> Bit:
        """This allows one to iterate over the bits in the collection."""

        for bit in self._bits:
            yield bit

    def __len__(self) -> int:
        """
        This overrides Python's built-in `len` function: it returns the number of bits.
        """

        return len(self._bits)

    def __str__(self) -> str:
        """
        This overrides Python's built-in `str` function: it returns a string
        representation of the collection of bits.
        """

        return " ".join(str(bit) for bit in self._bits)

    @property
    def max_length(self) -> int:
        """Get the maximum number of bits this can hold."""

        return self._max_length

    def pop_left(self) -> Bit:
        """
        This method will pop the left-most element in the collection. If there are no
        elements in the collection, then it will raise an error.

        This is a public method.

        Returns:
            bit:
                ...

        Raises:
            BitError:
                This bit string is empty.
        """

        if len(self) == 0:
            raise BitError("This bit string is empty!")

        ret: Bit = self._bits[0]
        self._bits = self._bits[1:]
        return ret

    def pop_right(self) -> Bit:
        """
        This method will pop the right-most element in the collection. If there are no
        elements in the collection, then it will raise an error.

        This is a public method.

        Returns:
            bit:
                ...

        Raises:
            BitError:
                This bit string is empty.
        """

        if len(self) == 0:
            raise BitError("This bit string is empty!")

        ret: Bit = self._bits[-1]
        self._bits = self._bits[:-1]
        return ret

    def push_left(self, bit: Bit) -> None:
        """
        This method will push a bit into the collection on the left. If the collection
        is full, then it will raise an error.

        This is a public method.

        Returns:
            bit:
                ...

        Raises:
            BitError:
                This bit string has the maximum number of bits allowed!
        """

        if len(self) == self._max_length:
            raise BitError("This bit string has the maximum number of bits allowed!")

        self._bits = [bit] + self._bits

    def push_right(self, bit: Bit) -> None:
        """
        This method will push a bit into the collection on the right. If the collection
        is full, then it will raise an error.

        This is a public method.

        Returns:
            bit:
                ...

        Raises:
            BitError:
                This bit string has the maximum number of bits allowed!
        """

        if len(self) == self._max_length:
            raise BitError("This bit string has the maximum number of bits allowed!")

        self._bits += [bit]
