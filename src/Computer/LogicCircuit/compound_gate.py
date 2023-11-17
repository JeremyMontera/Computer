import enum
from typing import Dict, Optional, Union

from Computer.LogicCircuit.abc import ILogicGate
from Computer.LogicCircuit.compound_factory import CompoundFactory
from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.LogicGate import LogicGate

PIN = Union[int, "Connection"]
# This represents everything that a pin can be connected to.
# TODO: replace `int` with `Bit` when ready, since bits will be passed around via the
# `Bit` class rather than integers.

STUFF = Union[LogicGate, Connection]


class CompoundType(enum.Enum):
    NAND: str = "nand"
    NOR: str = "nor"
    XOR: str = "xor"
    XNOR: str = "xnor"


class CompoundGateError(Exception):
    ...


class CompoundGate(ILogicGate):
    def __init__(self, type: Optional[CompoundType] = None, name: Optional[str] = None):
        if type is None or not isinstance(type, CompoundType):
            raise CompoundGateError("You need to enter a valid logic gate type!")

        self._type: CompoundType = type
        self._name: str = "" if name is None else name
        self._factory: CompoundFactory = CompoundFactory(type=type.value)

        manifest: Dict[str, STUFF] = self._factory.create()
        for key, value in manifest.items():
            setattr(self, f"_{key}", value)

    def get_output_pin(self):
        return self._output_gate.get_output_pin()

    def has_input_pin_set(self, pin: int = 0) -> bool:
        for gate in self._input_gates:
            if not gate.has_input_pin_set(pin=pin):
                return False
            
        return True

    def has_output_pin_set(self) -> bool:
        return self._output_gate.has_output_pin_set()

    def reset(self):
        # TODO: no good... don't want to access private attributes like this...
        ...

    def set_input_pin(self, value: int | Connection = 0, pin: int = 0) -> None:
        for gate in self._input_gates:
            gate.set_input_pin(value=value, pin=pin)

    def set_output_pin(self, value: Optional[Connection] = None) -> None:
        self._output_gate.set_output_pin(value=value)
