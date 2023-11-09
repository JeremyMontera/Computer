import enum
from typing import Union

BitValueType = Union[int, bool, str]


class BitValue(enum.Enum):
    OFF: int = 0
    ON: int = 1


class BitError(Exception):
    ...


class Bit:
    def __init__(self, value: BitValueType):
        self._value: BitValue = self._convert_to_bit_value(value)

    def __bool__(self) -> bool:
        if self._value == BitValue.OFF:
            return False
        elif self._value == BitValue.ON:
            return True

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self._value == BitValue.OFF:
            return "Bit(OFF)"
        elif self._value == BitValue.ON:
            return "Bit(ON)"

    def _convert_to_bit_value(self, value: BitValueType) -> BitValue:
        try:
            if int(value) == 0:
                return BitValue.OFF
            elif int(value) == 1:
                return BitValue.ON
            else:
                raise BitError(f"Entered an unknown value: {value}!")
        except ValueError:
            raise BitError("Entered something that cannot be handled!")
