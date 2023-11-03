from .logic_gate import LogicGateError
from .unary_gate import UnaryGate


class NotGate(UnaryGate):
    def __init__(self):
        super().__init__()

    def _logic(self) -> None:
        if self._input0_pin is None:
            raise LogicGateError("The first input pin has not been set!")

        output = not bool(self._input0_pin)

        print(f"[00:00:00] not {bool(self._input0_pin)} is {output}.")

        self._output_pin = int(output)
