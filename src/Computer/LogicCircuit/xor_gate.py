from typing import Optional, Union

from .Connection import Connection
from .LogicGate import AndGate
from .LogicGate.logic_gate import LogicGateError
from .nand_gate import NandGate


class XorGate:
    def __init__(self):
        self._input0_pin: Optional[Union[int, Connection]] = None
        self._input1_pin: Optional[Union[int, Connection]] = None
        self._output_pin: Optional[Union[int, Connection]] = None

        self._gate0: NandGate = NandGate()
        self._gate0.name = "xor :: nand gate"
        self._gate1: AndGate = AndGate()
        self._gate1.name = "xor :: and gate 0"
        self._gate2: AndGate = AndGate()
        self._gate2.name = "xor :: and gate 1"

        self._conn0: Connection = Connection()
        self._conn0.set_input_connection(self._gate0)
        self._conn0.set_output_connection(self._gate2, pin=0)
        self._conn1: Connection = Connection()
        self._conn1.set_input_connection(self._gate1)
        self._conn1.set_output_connection(self._gate2, pin=1)

        # TODO: add Branch here when implemented so don't need to call `set_input_pin`
        #       twice.

    def get_output_pin(self) -> int:
        return self._gate2.get_output_pin()

    def has_input_pin_set(self, pin: Optional[int] = 0) -> bool:
        if pin == 0:
            return self._input0_pin is not None
        elif pin == 1:
            return self._input1_pin is not None
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")

    def has_output_pin_set(self) -> bool:
        return self._output_pin is not None

    def set_input_pin(self, value: Union[int, "Connection"], pin: int = 0) -> None:
        print(f"[00:00:00] Setting {self._gate0.name}'s input pin {pin} to {value}.")
        self._gate0.set_input_pin(value, pin=pin)

        print(f"[00:00:00] Setting {self._gate0.name}'s input pin {pin} to {value}.")
        self._gate1.set_input_pin(value, pin=pin)
