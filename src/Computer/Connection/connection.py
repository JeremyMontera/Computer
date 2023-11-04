from typing import Optional

from Computer.LogicGate import LogicGate

class Connection:

    def __init__(self):
        self._input: Optional['LogicGate'] = None
        self._output: Optional['LogicGate'] = None

    def feed(self) -> int:
        ...

    def set_input(self, gate: 'LogicGate') -> None:
        ...

    def set_output(self, gate: 'LogicGate') -> None:
        ...