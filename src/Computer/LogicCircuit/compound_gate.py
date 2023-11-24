import enum
from typing import Dict, Optional, Union

from Computer.Bit.abc import IBit
from Computer.LogicCircuit.abc import ICompoundFactory, IConnection, ILogicGate
from Computer.LogicCircuit.compound_factory import CompoundFactory
from Computer.Logger import OUT

INFO = lambda msg: OUT.info(msg, level=2)
# Short-cut so we don't have to keep writing the same stuff...

PIN = Union[IBit, IConnection]
# This represents everything that a pin can be connected to.

STUFF = Union[ILogicGate, IConnection]
# This is a short-hand for the two types of devices used to build the compound gates.
# TODO: do we need to add `Branch` here for xor gates.


class CompoundType(enum.Enum):
    """
    This stores all the possible primitive Boolean logic gates that are currently
    supported. The user can only build on of these three gates.
    """

    NAND: str = "nand"
    """Build a NAND gate."""

    NOR: str = "nor"
    """Build a NOR gate."""

    XOR: str = "xor"
    """Build a XOR gate."""

    XNOR: str = "xnor"
    """Build a XNOR gate."""


class CompoundGateError(Exception):
    """Handle any errors associated with the `CompoundGate` class."""

    ...


class CompoundGate(ILogicGate):

    """
    This implements a compund logic gate, hiding any details about the underlying logic
    gates and wires making up the compound gate from the users. It is implemented using
    a factory design pattern: the user needs to pass a compound logic gate type when
    constructing a new instance. The factory will take the request and generate a
    manifest of the components needed to construct the compound gate.

    Attributes:
        type:           The type of compound logic gate (read-only)
        name:           The name of the compound logic gate (read and write)
        factory:        The factory used to generate the manifest (private)
        input_gates:    The gate(s) that will read in the information (private)
        output_gate:    The gate whose output will be read (private)
        gate<>:         Any intermediate gates needed to build the gate (private)
        conn<>:         Any wires needed to connect all of the gates (private)
    """

    def __init__(self, *, type: CompoundType, name: Optional[str] = None):
        """
        Constructor...

        Args:
            type:
                The type of compound logic gate.
            name:
                The name of the compound logic gate.
        """

        # Yay for not shooting ourselves in the foot... check to see if the user passed
        # a valid type to feed to the factory.
        if not isinstance(type, CompoundType):
            raise CompoundGateError("You need to enter a valid logic gate type!")
        
        INFO(f"Creating a new {type} compound logic gate with name {name}.")

        self._type: CompoundType = type
        """
        The type of compound logic gate.

        Type:
            CompoundType
        """

        self._name: str = "" if name is None else name
        """
        The name of the compound logic gate.

        Type:
            string
        """

        self._factory: ICompoundFactory = CompoundFactory(type=type.value)
        """
        The factory used to generate the manifest.

        Type:
            CompoundFactory
        """

        # Set `_input_gates`, `_output_gate` and any other intermediate gates or wires.
        manifest: Dict[str, STUFF] = self._factory.create()
        for key, value in manifest.items():
            setattr(self, f"_{key}", value)

    @property
    def name(self) -> str:
        """Read from the `name` attribute of the logic gate."""

        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """Write to the `name` attribute of the logic gate."""

        self._name = new_name

    @property
    def type(self) -> CompoundType:
        """Read from the `type` attribute of the logic gate."""

        return self._type

    def get_output_pin(self) -> IBit:
        """
        This will be the primary method called by the user. It will call the output
        gate's [`get_output_pin`][Computer.LogicCircuit.LogicGate] method and return the
        output.

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by other objects, such as `Connection`.

        Returns:
            result:
                ...
        """

        INFO(f"Getting the output of {self._name}.")
        return self._output_gate.get_output_pin()

    def has_input_pin_set(self, *, pin: int) -> bool:
        """
        This method will check to see if the input pin has been set yet. It will check
        all of the input gates by calling their
        [`has_input_pin_set`][Computer.LogicCircuit.LogicGate]. If any of them has not
        been set, it will return `'False'`, though this shouldn't normally happen.

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

        for gate in self._input_gates:
            if not gate.has_input_pin_set(pin=pin):
                return False

        return True

    def has_output_pin_set(self) -> bool:
        """
        This method will check to see if the output pin of the output gate has been set
        yet via [`has_output_pin_set`][Computer.LogicCircuit.LogicGate].

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called by some other object when constructing some
            circuit.

        Returns:
            flag:
                ...
        """

        return self._output_gate.has_output_pin_set()

    def reset(self, which: Optional[str] = None):
        """
        This method reset the input pins of the input gates and output pin of the
        output gate using [`reset()`][Computer.LogicCircuit.LogicGate]. This is mostly
        a convenience method to make testing smoother. It may not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            which:
                Which pins to reset.
        """

        def reset_inputs() -> None:
            """Helper function: reset input pins of input gate."""

            for gate in self._input_gates:
                gate.reset(which="input")

        def reset_output() -> None:
            """Helper function: reset input pins of input gate."""

            self._output_gate.reset(which="output")

        if which == "input":
            INFO(f"Resetting the input pins of {self._name}.")
            reset_inputs()
        elif which == "output":
            INFO(f"Resetting the output pins of {self._name}.")
            reset_output()
        else:
            INFO(f"Resetting the all of the pins of {self._name}.")
            reset_inputs()
            reset_output()

    def set_input_pin(self, *, value: IBit | IConnection, pin: int) -> None:
        """
        This method will set the input pins of the input gates using
        [`set_input_pin`][Computer.LogicCircuit.LogicGate]. It can either be directly
        given information (mostly used in the case of testing) or it can be given a
        `Connection` instance in order to form an association relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                What you want to set the input pin to.
            pin:
                The pin to set.
        """

        if isinstance(value, IBit):
            INFO(f"Setting input pin {pin} of {self._name} to bit {str(value)}.")
        elif isinstance(value, IConnection):
            INFO(f"Setting input pin {pin} of {self._name} to a connection.")

        for gate in self._input_gates:
            gate.set_input_pin(value=value, pin=pin)

    def set_output_pin(self, *, value: IConnection) -> None:
        """
        This method will set the output pin of the output gate using its
        [`set_output_pin`][Computer.LogicCircuit.LogicGate]. This method is to be used
        to mark that the output pin of the gate has been set and to establish the
        association relationship.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            value:
                The `Connection` instance you want to associate to this instance.
        """

        INFO(f"Setting the output pin of {self._name} to a connection.")
        self._output_gate.set_output_pin(value=value)
