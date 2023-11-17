from typing import Dict, Optional, Union

from Computer.LogicCircuit.LogicGate import LogicGate, LogicType
from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.abc import ICompoundFactory

STUFF = Union[LogicGate, Connection]


def create_nand_gate() -> Dict[str, STUFF]:
    gate0: LogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: LogicGate = LogicGate(type=LogicType.NOT, name="not_0")

    conn0: Connection = Connection()

    conn0.set_input_connection(gate=gate0)
    conn0.set_output_connection(gate=gate1, pin=0)

    return {"gate0": gate0, "gate1": gate1, "conn0": conn0}


def create_nor_gate() -> Dict[str, STUFF]:
    gate0: LogicGate = LogicGate(type=LogicType.OR, name="or_0")
    gate1: LogicGate = LogicGate(type=LogicType.NOT, name="not_0")

    conn0: Connection = Connection()

    conn0.set_input_connection(gate=gate0)
    conn0.set_output_connection(gate=gate1, pin=0)

    return {"gate0": gate0, "gate1": gate1, "conn0": conn0}


def create_xor_gate() -> Dict[str, STUFF]:
    gate0: LogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: LogicGate = LogicGate(type=LogicType.NOT, name="not_0")
    gate2: LogicGate = LogicGate(type=LogicType.AND, name="and_1")
    gate3: LogicGate = LogicGate(type=LogicType.AND, name="and_2")

    conn0: Connection = Connection()
    conn1: Connection = Connection()
    conn2: Connection = Connection()

    conn0.set_input_connection(gate=gate0)
    conn0.set_output_connection(gate=gate1, pin=0)

    conn1.set_input_connection(gate=gate1)
    conn1.set_output_connection(gate=gate3, pin=0)

    conn2.set_input_connection(gate=gate2)
    conn2.set_output_connection(gate=gate3, pin=1)

    return {
        "gate0": gate0,
        "gate1": gate1,
        "gate2": gate2,
        "gate3": gate3,
        "conn0": conn0,
        "conn1": conn1,
        "conn2": conn2,
    }


def create_xnor_gate() -> Dict[str, STUFF]:
    gate0: LogicGate = LogicGate(type=LogicType.AND, name="and_0")
    gate1: LogicGate = LogicGate(type=LogicType.NOT, name="not_0")
    gate2: LogicGate = LogicGate(type=LogicType.AND, name="and_1")
    gate3: LogicGate = LogicGate(type=LogicType.AND, name="and_2")
    gate4: LogicGate = LogicGate(type=LogicType.NOT, name="not_1")

    conn0: Connection = Connection()
    conn1: Connection = Connection()
    conn2: Connection = Connection()
    conn3: Connection = Connection()

    conn0.set_input_connection(gate=gate0)
    conn0.set_output_connection(gate=gate1, pin=0)

    conn1.set_input_connection(gate=gate1)
    conn1.set_output_connection(gate=gate3, pin=0)

    conn2.set_input_connection(gate=gate2)
    conn2.set_output_connection(gate=gate3, pin=1)

    conn3.set_input_connection(gate=gate3)
    conn3.set_output_connection(gate=gate4, pin=0)

    return {
        "gate0": gate0,
        "gate1": gate1,
        "gate2": gate2,
        "gate3": gate3,
        "gate4": gate4,
        "conn0": conn0,
        "conn1": conn1,
        "conn2": conn2,
        "conn3": conn3,
    }


class CompoundError(Exception):
    ...


class CompoundFactory(ICompoundFactory):
    factories = {
        "xor": create_xor_gate,
        "xnor": create_xnor_gate,
        "nand": create_nand_gate,
        "nor": create_nor_gate,
    }

    def __init__(self, type: Optional[str] = None):
        if type is None or type not in list(self.factories.keys()):
            raise CompoundError("You need to pass a valid compound logic gate type!")

        self._type: str = type

    def create(self) -> Dict[str, STUFF]:
        return self.factories[self._type]()
