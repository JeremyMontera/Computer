from __future__ import annotations

import enum
from typing import Union

from Computer.Bit.abc import IBit

BitValueType = Union[int, bool, str]


class BitValue(enum.Enum):
    """This controls the value that the bits can take. This is assumed to be an
    enumeration type."""

    OFF: int = 0
    """
    The off/0/false bit value.
    """

    ON: int = 1
    """
    The on/1/true bit value.
    """


class BitError(Exception):
    ...


class Bit(IBit):

    """
    This implements a bit class. This ensures that the user doesn't send bad data
    along the circuitry. It simply holds the intended value the user wants to send.

    Attributes:
        value: the value of the bit (private)
    """

    def __init__(self, value: BitValueType):
        """
        Constructor...

        Args:
            value:
                The value of the bit.
        """

        self._value: BitValue = self._convert_to_bit_value(value)
        """
        The value of the bit.

        Type:
            BitValue
        """

    def __eq__(self, other: Bit) -> bool:
        """
        Overrides Python's `'=='` operator: checks if two bits are the same.

        Args:
            other:
                ...

        Returns:
            flag:
                ...
        """

        return self._value == other._value

    def __str__(self) -> str:
        """A string representation of the bit."""

        if self._value == BitValue.OFF:
            return "Bit(OFF)"
        elif self._value == BitValue.ON:
            return "Bit(ON)"

    def _convert_to_bit_value(self, value: BitValueType) -> BitValue:
        """
        This will try to convert the value inputted by the user into a `BitValue` enum
        type. Valid `value` types include integers, strings, or other Boolean values.
        This will attempt to first convert `value` into an integer. It will then check
        to see if the value is either zero or one.

        This is a private method.

        Args:
            value:
                ...

        Returns:
            ret:
                ...

        Raises:
            BitError:
                (1) Entered an unknown value: {value}!
                (2) Entered something that cannot be handled!
        """

        try:
            if int(value) == 0:
                return BitValue.OFF
            elif int(value) == 1:
                return BitValue.ON
            else:
                raise BitError(f"Entered an unknown value: {value}!")
        except (ValueError, TypeError):
            raise BitError("Entered something that cannot be handled!")

    def and_op(self, other: Bit) -> Bit:
        """
        This implements a custom `'and'` operation: returns an `'ON'` bit only if both
        the input bits are `'ON'`.

        Args:
            other:
                ...

        Returns:
            ret:
                ...
        """

        return Bit(self._value.value and other._value.value)

    def not_op(self) -> Bit:
        """
        This implements a custom `'not'` operation: reverses the current bit.

        Returns:
            ret:
                ...
        """

        return Bit(not self._value.value)

    def or_op(self, other: Bit) -> Bit:
        """
        This implements a custom `'or'` operation: returns an `'OFF'` bit only if both
        the input bits are `'OFF'`.

        Args:
            other:
                ...

        Returns:
            ret:
                ...
        """

        return Bit(self._value.value or other._value.value)
