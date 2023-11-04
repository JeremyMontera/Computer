from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from Computer.LogicGate import LogicGate

class ConnectionError(Exception):
    ...

class Connection:

    def __init__(self):
        self._input: Optional['LogicGate'] = None
        self._output: Optional['LogicGate'] = None

    def feed(self) -> int:
        if self._input is None:
            raise ConnectionError("The output hasn't been connected yet!")
        
        print(f"[00:00:00] Feeding input gate {self._input.name}'s output.")
        return self._input.get_output_pin()

    def set_input(self, gate: 'LogicGate') -> None:
        if gate.has_output_set():
            raise ConnectionError(f"{gate.name}'s output pin is already set!")
        
        print(f"[00:00:00] Setting {gate.name}'s output pin to the input.")
        self._input = gate

    def set_output(self, gate: 'LogicGate') -> None:
        if not gate.has_input_set(pin=0):
            gate.set_input_pin(self, pin=0)
        elif gate.type == "binary":
            if not gate.has_input_set(pin=1):
                gate.set_input_pin(self, pin=1)
        else:
            raise ConnectionError(f"{gate.name}'s input pin(s) are already set!")