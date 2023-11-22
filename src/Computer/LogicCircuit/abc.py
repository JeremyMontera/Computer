from __future__ import annotations

import abc
import enum
from typing import Dict, Optional, TypeVar

from Computer.Bit.abc import IBit

T = TypeVar("T")
# This is to represent arbitrary devices.

E = TypeVar("E", bound=enum.Enum)
# This is to represent an arbitrary enumeration type.


class ICompoundFactory(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def __init__(self, *, type: str):
        """Constructor..."""

        ...

    @abc.abstractclassmethod
    def create(self) -> Dict[str, T]:
        """This creates the manifest."""

        ...


class IConnection(metaclass=abc.ABCMeta):

    """
    This implements a wire connecting two other devices, where it feeds data from the
    input to the output.
    """

    @abc.abstractclassmethod
    def __init__(self):
        """Constructor..."""

        ...

    @abc.abstractclassmethod
    def feed(self) -> IBit:
        """This gets the information from the input and returns it."""

        ...

    @abc.abstractclassmethod
    def has_input_connection_set(self) -> bool:
        """This will check if there is an input device."""

        ...

    @abc.abstractclassmethod
    def has_output_connection_set(self) -> bool:
        """This will check if there is an output device."""

        ...

    @abc.abstractclassmethod
    def reset(self) -> None:
        """This will reset the wire."""

        ...

    @abc.abstractclassmethod
    def set_input_connection(self, *, device: ILogicGate | IBranch | ISwitch) -> None:
        """This will establish an input connection with a device."""

        ...

    @abc.abstractclassmethod
    def set_output_connection(
        self, *, device: ILogicGate| IBranch | ISwitch, index: int
    ) -> None:
        """This will establish an output connection with a device."""

        ...


class IBranch(IConnection, metaclass=abc.ABCMeta):

    """
    This implements a branching connection: multiple wires comming in and multiple
    wires going out of a single junction.
    """

    @abc.abstractclassmethod
    def feed(self, *, index: int) -> IBit:
        """This gets the information from the appropriate input and returns it."""

        ...

    @abc.abstractclassmethod
    def has_mapping_set(self) -> bool:
        """This method will check to see if the mapping has been set yet."""

        ...

    @abc.abstractclassmethod
    def set_input_connection(self, *, conn: IConnection) -> None:
        """This will establish an input connection with a device."""

        ...

    @abc.abstractclassmethod
    def set_mapping(self, *, mapping: Dict[int, int]) -> None:
        """This will establish a mapping between outputs and inputs."""

        ...

    @abc.abstractclassmethod
    def set_output_connection(self, *, conn: IConnection) -> None:
        """This will establish an output connection with a device."""

        ...

class ISwitch(IConnection, metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def has_input_connection_set(self, *, index: int) -> bool:
        """This will check if there is an input device."""

        ...

    @abc.abstractclassmethod
    def set_input_connection(self, *, conn: IConnection, index: int) -> None:
        """This will establish an input connection with a device."""

        ...

    @abc.abstractclassmethod
    def set_output_connection(self, *, conn: IConnection) -> None:
        """This will establish an output connection with a device."""

        ...


class ILogicGate(metaclass=abc.ABCMeta):

    """
    This implements the interface for a logic gate, hiding any details about the
    underlying transistors from the users.
    """

    @abc.abstractclassmethod
    def __init__(self, *, type: E, name: Optional[str] = None):
        """Constructor..."""

        ...

    @abc.abstractclassmethod
    def get_output_pin(self) -> IBit:
        """This gets the output of performing the logic on the input(s)."""

        ...

    @abc.abstractclassmethod
    def has_input_pin_set(self, *, pin: int) -> bool:
        """This checks if the input pin has been set."""

        ...

    @abc.abstractclassmethod
    def has_output_pin_set(self) -> bool:
        """This checks if the output pin has been set."""

        ...

    @abc.abstractclassmethod
    def reset(self, which: Optional[str] = None) -> None:
        """This resets the input and output pins."""

        ...

    @abc.abstractclassmethod
    def set_input_pin(self, *, value: IBit | IConnection, pin: int) -> None:
        """This sets the input pin."""

        ...

    @abc.abstractclassmethod
    def set_output_pin(self, *, value: IConnection) -> None:
        """This sets the output pin."""

        ...
