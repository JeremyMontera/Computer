from typing import Optional

from .logic_gate import LogicGate, LogicGateError

class UnaryGate(LogicGate):
    def __init__(self):
        super().__init__()
        self._input0_pin: Optional[int] = None

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        if pin == 0:
            if self._input0_pin is not None:
                raise LogicGateError("Input pin 0 has already been set!")
            else:
                self._input0_pin = value
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")