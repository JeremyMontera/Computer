import enum
from typing import List, Optional, Union, cast

from Computer.Bit import Bit
from Computer.LogicCircuit.abc import IConnection, ILogicGate
from Computer.Logger import OUT

INFO = lambda msg: OUT.info(msg, level=0)
# Short-cut so we don't have to keep writing the same stuff...

PIN = Union[Bit, IConnection]
# This represents everything that a pin can be connected to.


class LogicType(enum.Enum):
    """
    This stores all the possible primitive Boolean logic gates that are currently
    supported. The user can only build on of these three gates.
    """

    NOT: str = "not"
    """Build a NOT gate."""

    AND: str = "and"
    """Build an AND gate."""

    OR: str = "or"
    """Build an OR gate."""


class LogicGateError(Exception):
    """Handle any errors associated with the `LogicGate` class."""

    ...


class LogicGate(ILogicGate):

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

    mapping = {LogicType.NOT: 1, LogicType.AND: 2, LogicType.OR: 2}
    # Added mapping here because enum's giving me issues.

    def __init__(self, *, type: LogicType, name: Optional[str] = None):
        """
        Constructor...

        Args:
            type:
                The type of logic gate. Note that while this is marked as `Optional`,
                this will raise a `LogicGateError` if not passed a valid type.
            name:
                The name of the logic gate.
        """

        # Check to see if the user screwed up and didn't pass a valid type (don't shoot
        # ourselves in the foot).
        if not isinstance(type, LogicType):
            raise LogicGateError("You need to pass a valid logic gate type!")
        
        INFO(f"Creating a new {type} logic gate with name {name}.")

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

        self._input_pins: List[Optional[PIN]] = [cast(PIN, None)] * self.mapping[
            self._type
        ]
        """
        The input pins for information to come in.

        Type:
            List[Optional[Bit | IConnection]]
        """

        self._output_pin: Optional[IConnection] = cast(PIN, None)
        """
        The output pin for information to leave.

        Type:
            List[Optional[IConnection]]
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

    def get_output_pin(self) -> Bit:
        """
        This will be the primary method called by the user. It will first get all the
        requisite inputs for the type of logic gate built sequentially. Then, depending
        on the type of logic gate, it will perform whatever logically operation is
        requested. It will then return the results.

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by other objects, such as `IConnection`.

        Returns:
            result:
                ...
        """

        INFO(f"Getting the output of {self._name}.")

        # Get the input pin information
        inputs: List[Bit] = [None] * self.mapping[self._type]
        for p, pin in enumerate(self._input_pins):
            if pin is None:
                raise LogicGateError(f"Pin {p} has not been set yet!")
            elif isinstance(pin, IConnection):
                inputs[p] = pin.feed()
            elif isinstance(pin, Bit):
                inputs[p] = pin

        INFO(f"The inputs have been set to: {[str(inp) for inp in inputs]}.")

        # Process the input pins
        if self._type == LogicType.NOT:
            output: Bit = inputs[0].not_op()
        elif self._type == LogicType.AND:
            output: Bit = inputs[0].and_op(inputs[1])
        elif self._type == LogicType.OR:
            output: Bit = inputs[0].or_op(inputs[1])

        INFO(f"The resulting output is: {output}.")
        return output

    def has_input_pin_set(self, *, pin: int) -> bool:
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

    def reset(self, which: Optional[str] = None) -> None:
        """
        This method reset the input and output pins. This is mostly a convenience
        method to make testing smoother. It may not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            which:
                Which pins to reset.
        """

        if which == "input":
            INFO(f"Resetting the input pins of {self._name}.")
            self._input_pins = [None] * self.mapping[self._type]
        elif which == "output":
            INFO(f"Resetting the output pins of {self._name}.")
            self._output_pin = None
        else:
            INFO(f"Resetting the all of the pins of {self._name}.")
            self._input_pins = [None] * self.mapping[self._type]
            self._output_pin = None

    def set_input_pin(self, *, value: Bit | IConnection, pin: int) -> None:
        """
        This method will set the input pin. It can either be directly given information
        (mostly used in the case of testing) or it can be given a `IConnection` instance
        in order to form an association relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                What you want to set the input pin to.
            pin:
                The pin to set.
        """

        # Check to see if the input pin has been set yet (yupp, again, making sure we
        # don't shoot ourselves again...)
        if self.has_input_pin_set(pin=pin):
            raise LogicGateError(f"Input pin {pin} has already been set!")

        if isinstance(value, Bit):
            INFO(f"Setting input pin {pin} of {self._name} to bit {str(value)}.")
        elif isinstance(value, IConnection):
            INFO(f"Setting input pin {pin} of {self._name} to a connection.")

        self._input_pins[pin] = value

    def set_output_pin(self, *, value: IConnection) -> None:
        """
        This method will set the output pin. This method is to be used to mark that the
        output pin of the gate has been set and to establish the association
        relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                The `IConnection` instance you want to associate to this instance.
        """

        # Can we shoot ourselves in the foot by trying to set this instance when it has
        # already been set?
        if self.has_output_pin_set():
            raise LogicGateError("The output pin has already been set!")

        INFO(f"Setting the output pin of {self._name} to a connection.")
        self._output_pin = value
