from typing import Optional, Union

from .Connection import Connection
from .LogicGate import NotGate
from .LogicGate.logic_gate import LogicGateError
from .xor_gate import XorGate


class XnorGate:
    def __init__(self):
        self._input0_pin: Optional[Union[int, Connection]] = None
        self._input1_pin: Optional[Union[int, Connection]] = None
        self._output_pin: Optional[Union[int, Connection]] = None

        self._gate0: XorGate = XorGate()
        self._gate0.name = "xnor :: xor gate"
        self._gate1: NotGate = NotGate()
        self._gate1.name = "xnor :: not gate"

        self._conn0: Connection = Connection()
        self._conn0.set_input_connection(self._gate0)
        self._conn0.set_output_connection(self._gate1)

    def get_output_pin(self) -> int:
        return self._gate1.get_output_pin()

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
        self._gate0.set_input_pin(value, pin=pin)
