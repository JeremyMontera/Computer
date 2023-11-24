from typing import Dict, Union

from Computer.Logger import OUT
from Computer.LogicCircuit.abc import ICompoundFactory, IConnection, ILogicGate
from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.LogicGate import LogicGate, LogicType

INFO = lambda msg: OUT.info(msg, level=1)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

STUFF = Union[ILogicGate, IConnection]
# This is a short-hand for the two types of devices used to build the compound gates.
# TODO: do we need to add `Branch` here for xor gates.


def create_nand_gate() -> Dict[str, STUFF]:
    """
    This function will create a manifest for what nand gates need when created.

    NOTE:
        This function is marked public and can be called by the user, though it is more
        likely to be called in [`create()`][`Computer.LogicCircuit.CompoundFactory`].

    Returns:
        manifest:
            A dictionary of all the components needed to construct the nand gate.
    """

    # The logic gates needed...
    gate0: ILogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: ILogicGate = LogicGate(type=LogicType.NOT, name="not_0")

    # The wires needed...
    conn0: IConnection = Connection()

    # Establish all of the association relationships between the logic gates and wires.
    conn0.set_input_connection(device=gate0)
    conn0.set_output_connection(device=gate1, index=0)

    return {"input_gates": [gate0], "output_gate": gate1, "conn0": conn0}


def create_nor_gate() -> Dict[str, STUFF]:
    """
    This function will create a manifest for what nor gates need when created.

    NOTE:
        This function is marked public and can be called by the user, though it is more
        likely to be called in [`create()`][`Computer.LogicCircuit.CompoundFactory`].

    Returns:
        manifest:
            A dictionary of all the components needed to construct the nor gate.
    """

    # The logic gates needed...
    gate0: ILogicGate = LogicGate(type=LogicType.OR, name="or_0")
    gate1: ILogicGate = LogicGate(type=LogicType.NOT, name="not_0")

    # The wires needed...
    conn0: IConnection = Connection()

    # Establish all of the association relationships between the logic gates and wires.
    conn0.set_input_connection(device=gate0)
    conn0.set_output_connection(device=gate1, index=0)

    return {"input_gates": [gate0], "output_gate": gate1, "conn0": conn0}


def create_xor_gate() -> Dict[str, STUFF]:
    """
    This function will create a manifest for what xor gates need when created.

    NOTE:
        This function is marked public and can be called by the user, though it is more
        likely to be called in [`create()`][`Computer.LogicCircuit.CompoundFactory`].

    Returns:
        manifest:
            A dictionary of all the components needed to construct the xor gate.
    """

    # The logic gates needed...
    gate0: ILogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: ILogicGate = LogicGate(type=LogicType.NOT, name="not_0")
    gate2: ILogicGate = LogicGate(type=LogicType.OR, name="or_0")
    gate3: ILogicGate = LogicGate(type=LogicType.AND, name="and_1")

    # The wires needed...
    conn0: IConnection = Connection()
    conn1: IConnection = Connection()
    conn2: IConnection = Connection()

    # Establish all of the association relationships between the logic gates and wires.
    # For the first wire... NB: this is a nand gate in disguise.
    conn0.set_input_connection(device=gate0)
    conn0.set_output_connection(device=gate1, index=0)

    # For the second wire...
    conn1.set_input_connection(device=gate1)
    conn1.set_output_connection(device=gate3, index=0)

    # For the third wire...
    conn2.set_input_connection(device=gate2)
    conn2.set_output_connection(device=gate3, index=1)

    return {
        "input_gates": [gate0, gate2],
        "gate1": gate1,
        "output_gate": gate3,
        "conn0": conn0,
        "conn1": conn1,
        "conn2": conn2,
    }


def create_xnor_gate() -> Dict[str, STUFF]:
    """
    This function will create a manifest for what xnor gates need when created.

    NOTE:
        This function is marked public and can be called by the user, though it is more
        likely to be called in [`create()`][`Computer.LogicCircuit.CompoundFactory`].

    Returns:
        manifest:
            A dictionary of all the components needed to construct the xnor gate.
    """

    # The logic gates needed...
    gate0: ILogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: ILogicGate = LogicGate(type=LogicType.NOT, name="not_0")
    gate2: ILogicGate = LogicGate(type=LogicType.OR, name="or_0")
    gate3: ILogicGate = LogicGate(type=LogicType.AND, name="and_1")
    gate4: ILogicGate = LogicGate(type=LogicType.NOT, name="not_1")

    # The wires needed...
    conn0: IConnection = Connection()
    conn1: IConnection = Connection()
    conn2: IConnection = Connection()
    conn3: IConnection = Connection()

    # Establish all of the association relationships between the logic gates and wires.
    # For the first wire... NB: this is a nand gate in disguise.
    conn0.set_input_connection(device=gate0)
    conn0.set_output_connection(device=gate1, index=0)

    # For the second wire...
    conn1.set_input_connection(device=gate1)
    conn1.set_output_connection(device=gate3, index=0)

    # For the third wire...
    conn2.set_input_connection(device=gate2)
    conn2.set_output_connection(device=gate3, index=1)

    # For the fourth wire...
    conn3.set_input_connection(device=gate3)
    conn3.set_output_connection(device=gate4, index=0)

    return {
        "input_gates": [gate0, gate2],
        "gate1": gate1,
        "gate2": gate3,
        "output_gate": gate4,
        "conn0": conn0,
        "conn1": conn1,
        "conn2": conn2,
        "conn3": conn3,
    }


class CompoundFactoryError(Exception):
    """Handle any errors associated with the `CompoundFactory` class."""

    ...


class CompoundFactory(ICompoundFactory):

    """
    This implements a factory design pattern for constructing new compound logic gates.
    This simplifies their implementation since now you only need to specify the layout
    of the wires and logic gates once, behind the scenes, and this factory will handle
    the rest.

    Attributes:
        type:       What type of compound gate is being requested (private)
        factories:  Map of known compound gates to their create functions (private)
    """

    _factories = {
        "xor": create_xor_gate,
        "xnor": create_xnor_gate,
        "nand": create_nand_gate,
        "nor": create_nor_gate,
    }
    """
    Map of known compound gates to their create functions.

    Type:
        dict[string, callable]
    """

    def __init__(self, *, type: str):
        """
        Constructor...

        Arg:
            type:
                What type of compound gate is being requested.
        """

        INFO(f"Creating a new {type} compound factory.")

        self._type: str = type
        """
        What type of compound gate is being requested.

        Type:
            string
        """

    def create(self) -> Dict[str, STUFF]:
        """
        This will call the corresponding create function to return a manifest of
        components needed to build the compound gate.

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called in the constructor of `CompoundGate`.

        Returns:
            manifest:
                A dictionary of all the components needed to construct the gate.
        """

        INFO(f"Building the manifest for a {self._type} compound logic gate.")
        return self._factories[self._type]()
