from typing import Optional

from Computer.LogicGate import LogicGate

class ConnectionError(Exception):
    ...

class Connection:

    def __init__(self):
        self._input: Optional['LogicGate'] = None
        self._output: Optional['LogicGate'] = None

    def feed(self) -> int:
        if self._output is None:
            raise ConnectionError("The output hasn't been connected yet!")
        
        print(f"[00:00:00] Feeding input gate {self._input.name}'s output.")
        return self._input.get_output_pin()

    def set_input(self, gate: 'LogicGate') -> None:
        if gate.has_output_set():
            raise ConnectionError(f"{gate.name}'s output pin is already set!")
        
        print(f"[00:00:00] Setting {gate.name}'s output pin to the input.")
        self._input = gate

    def set_output(self, gate: 'LogicGate') -> None:
        ...