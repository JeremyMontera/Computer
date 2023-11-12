import abc
from typing import TYPE_CHECKING, Optional, Union, List, cast

if TYPE_CHECKING:
    from Computer.LogicCircuit.Connection import Connection

PIN = Optional[Union[int, 'Connection']]


class LogicGateError(Exception):
    ...


class ILogicGate(metaclass=abc.ABCMeta):

    """
    This implements an interface for the `LogicGate` class. This will encompase both
    binary and unary gate definitions.

    Attributes:
        input_pins:     the list of all possible input pins (private)
        name:           the name of the logic gate (public)
        output_pin:     the output pin (private)
    """

    @abc.abstractclassmethod
    def __init__(self):
        """Constructor..."""

        self._input_pin: List[PIN] = cast(List, None)
        """
        The list of all possible input pins.

        Type:
            List[int | Connection]
        """

        self._name: str = ""
        """
        The name of the logic gate.

        Type:
            string
        """

        self._output_pin: PIN = None
        """
        The output pin.

        Type:
            integer | Connection
        """

    @property
    def name(self) -> str:
        """The name of the logic gate."""

        ...

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the logic gate."""

        ...

    @abc.abstractclassmethod
    def _logic(self) -> None:
        """
        This implements how the inputs get transformed into the output.

        This is a private method not intended to be directly called by the user.
        """

        ...

    @abc.abstractclassmethod
    def _sanitize_input(self, value: Union[int, "Connection"]) -> None:
        """
        This will check the values being set to the input pins. Since inputs are
        assumed to be binary, it checks if the input is 0/1. This is called when
        `set_input_pin` is called by one of the descendants.

        This is a private method not intended to be directly called by the user.

        Raises:
            {value} is not a valid input!

        Args:
            value:
                The value to be inputted to the logic gate.
        """

        ...

    @abc.abstractclassmethod
    def get_output_pin(self) -> int:
        """
        This will get the value of the output pin. This will first run the logic of the
        logic gate to compute the output. Since `_logic` is assumed to be private, and
        `_output_pin` is private, it is assumed that the user will not have been able
        to set the value of the output. However, it will bypass this `_logic` call if
        `_output_pin` is not `'None'`.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an output that has
        this method implemented for polymorphism.

        Returns:
            output_pin:
                The value of the output after the logic has been applied to the values
                held by the input pins.
        """

        ...

    @abc.abstractclassmethod
    def has_input_pin_set(self, pin: Optional[int] = 0) -> bool:
        """
        This will check to see if the requested input pin has been set yet.

        This is a public method that can be called by the user, but more than likely,
        it will be called by the `Connection` class.

        Args:
            pin:
                (Optional) The pin to check. This defaults to pin 0.
        """

        ...

    @abc.abstractclassmethod
    def has_output_pin_set(self) -> bool:
        """
        This will check to see if the output pin has been set yet. Most of the time,
        the expectation is that this is not set.

        This is a public method that can be called by the user, but more than likely,
        it will be called by the `Connection` class.

        Returns:
            flag:
                ...
        """

        ...

    @abc.abstractclassmethod
    def set_input_pin(self, value: Union[int, "Connection"], pin: int = 0) -> None:
        """
        This will set the input pins.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an input that has
        this method implemented for polymorphism.

        Args:
            value:
                The value to set the pin to.
            pin:
                (Optional) the pin to set the value to. This defaults to zero to
                handle the case of unary gates.
        """

        ...
