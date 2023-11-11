from typing import Optional, Union

from .LogicGate import AndGate, NotGate
from .Connection import Connection

class NandGate():

    def __init__(self):
        self._input0_pin: Optional[Union[int, Connection]] = None
        self._input1_pin: Optional[Union[int, Connection]] = None
        self._output_pin: Optional[Union[int, Connection]] = None

        self._gate0: AndGate = AndGate()
        self._gate0.name = "and gate"
        self._gate1: NotGate = NotGate()
        self._gate1.name = "not gate"
        
        self._conn0: Connection = Connection()
        self._conn0.set_input_connection(self._gate0)
        self._conn0.set_output_connection(self._gate1)

    def set_input_pin(self, value: Union[int, "Connection"], pin: int = 0) -> None:
        self._gate0.set_input_pin(value, pin=pin)

    def get_output_pin(self) -> int:
        return self._gate1.get_output_pin()
