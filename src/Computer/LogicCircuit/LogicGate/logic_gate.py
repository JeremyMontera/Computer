import enum
from typing import List, Optional, Union, cast

from Computer.LogicCircuit import abc
from Computer.LogicCircuit.Connection import Connection

PIN = Union[int, "Connection"]
# This represents everything that a pin can be connected to.
# TODO: replace `int` with `Bit` when ready, since bits will be passed around via the
# `Bit` class rather than integers.


class LogicType(enum.Enum):
    """
    This stores all the possible primitive Boolean logic gates that are currently
    supported. The user can only build on of these three gates. The value of each
    enumeration corresponds to the number of input pins that the gate needs.
    """

    NOT: int = 1
    """Build a NOT gate."""

    AND: int = 2
    """Build an AND gate."""

    OR: int = 2
    """Build an OR gate."""


class LogicGateError(Exception):
    """Handle any errors associated with the `LogicGate` class."""

    ...


class LogicGate(abc.ILogicGate):

    """
    This implements a logic gate, hiding any details about the underlying transistors
    from the users. It is implemented using a psuedo-builder design pattern: the user
    needs to pass a logic gate type when constructing a new instance, and it will
    assign the needed number of input pins at construction time. This type option will
    also determine which logic is performed.

    Attributes:
        type:       The type of logic gate (read-only)
        name:       The name of the logic gate (read and write)
        input_pins: The input pins for information to come in (private)
        output_pin: The output pin for information to leave (private)
    """

    def __init__(self, type: Optional[LogicType] = None, name: Optional[str] = None):
        """
        Constructor...

        Args:
            type:
                The type of logic gate. Note that while this is marked as `Optional`,
                this will raise a `LogicGateError` if not passed a valid type.
            name:
                The name of the logic gate.
        """

        # Check to see if the user forgot to pass a `type` or if the user screwed up
        # and didn't pass a valid type (don't shoot ourselves in the foot).
        if type is None or not isinstance(type, LogicType):
            raise LogicGateError("You need to pass a valid logic gate type!")

        self._type: LogicType = type
        """
        The type of logic gate.

        Type:
            LogicType
        """

        self._name: str = "" if name is None else name
        """
        The name of the logic gate.

        Type:
            string
        """

        self._input_pins: List[Optional[PIN]] = [cast(PIN, None)] * self._type.value
        """
        The input pins for information to come in.

        Type:
            List[Optional[integer | Connection]]
        """

        self._output_pin: Optional["Connection"] = cast(PIN, None)
        """
        The output pin for information to leave.

        Type:
            List[Optional[Connection]]
        """

    @property
    def name(self) -> str:
        """Read from the `name` attribute of the logic gate."""

        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Write to the `name` attribute of the logic gate."""

        self._name = new_name

    @property
    def type(self) -> LogicType:
        """Read from the `type` attribute of the logic gate."""

        return self._type

    def _sanitize_input(self, value: int | Connection) -> None:
        """
        This will check to see if the user fed the logic gate a valid input. Since the
        input pins can be either an integer or a `Connection` instance, then this will
        only validate in the case of an integer, and assume that the input is validated
        higher up the chain.

        NOTE:
            This method is marked private and should not be directly called.

        TODO: update when `Bit` can be passed around.

        Args:
            value:
                ...
        """

        if isinstance(value, int):
            assert value in [0, 1], f"{value} is not a valid input!"

    def get_output_pin(self) -> int:
        """
        This will be the primary method called by the user. It will first get all the
        requisite inputs for the type of logic gate built sequentially. Then, depending
        on the type of logic gate, it will perform whatever logically operation is
        requested. It will then return the results.

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by other objects, such as `Connection`.

        TODO: update when `Bit` can be passed around.

        Returns:
            result:
                ...
        """

        # Get the input pin information
        inputs: List[int] = [None] * self._type.value
        for p, pin in enumerate(self._input_pins):
            if pin is None:
                raise LogicGateError(f"Pin {p} has not been set yet!")
            elif isinstance(pin, Connection):
                inputs[p] = pin.feed()
            elif isinstance(pin, int):
                inputs[p] = pin

        # Process the input pins
        if self._type == LogicType.NOT:
            output: bool = not bool(inputs[0])
        elif self._type == LogicType.AND:
            output: bool = bool(inputs[0]) and bool(inputs[1])
        elif self._type == LogicType.OR:
            output: bool = bool(inputs[0]) or bool(inputs[1])

        # Return the results
        return int(output)

    def has_input_pin_set(self, pin: int = 0) -> bool:
        """
        This method will check to see if the input pin has been set yet.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called by some other object when constructing some
            circuit.

        Args:
            pin:
                What pin to check.

        Returns:
            flag:
                ...
        """

        # Check to see if the pin is a valid pin (again, to keep from shooting
        # ourselves in the foot).
        if pin not in list(range(len(self._input_pins))):
            raise LogicGateError(f"Entered an invalid pin: {pin}!")

        return self._input_pins[pin] is not None

    def has_output_pin_set(self) -> bool:
        """
        This method will check to see if the output pin has been set yet.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called by some other object when constructing some
            circuit.

        Returns:
            flag:
                ...
        """

        return self._output_pin is not None

    def reset(self) -> None:
        """
        This method reset the input and output pins. This is mostly a convenience
        method to make testing smoother. It may not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.
        """

        self._input_pins = [None] * self._type.value
        self._output_pin = None

    def set_input_pin(self, value: int | Connection = 0, pin: int = 0) -> None:
        """
        This method will set the input pin. It can either be directly given information
        (mostly used in the case of testing) or it can be given a `Connection` instance
        in order to form an association relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                What you want to set the input pin to.
            pin:
                The pin to set.
        """

        self._sanitize_input(pin)

        # Check to see if the input pin has been set yet (yupp, again, making sure we
        # don't shoot ourselves again...)
        if self.has_input_pin_set(pin):
            raise LogicGateError(f"Input pin {pin} has already been set!")

        self._input_pins[pin] = value

    def set_output_pin(self, value: Optional[Connection] = None) -> None:
        """
        This method will set the output pin. This method is to be used to mark that the
        output pin of the gate has been set and to establish the association
        relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                The `Connection` instance you want to associate to this instance.
        """

        # Can we shoot ourselves in the foot by not passing anything?
        if value is None:
            raise LogicGateError("You need to enter a valid connection!")

        # ... or can we by trying to set this instance when it has already been set?
        if self.has_output_pin_set():
            raise LogicGateError("The output pin has already been set!")

        self._output_pin = value
