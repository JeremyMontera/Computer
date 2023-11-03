from .binary_gate import BinaryGate
from .logic_gate import LogicGateError

class AndGate(BinaryGate):
    
    def __init__(self):
        super().__init__()

    def _logic(self) -> None:
        if self._input0_pin is None:
            raise LogicGateError("The first input pin has not been set!")
        elif self._input1_pin is None:
            raise LogicGateError("The second input pin has not been set!")
        
        output = bool(self._input0_pin) and bool(self._input1_pin)

        print(
            f"[00:00:00] {bool(self._input0_pin)} and {bool(self._input1_pin)} is " \
            f"{output}."
        )
        
        return output