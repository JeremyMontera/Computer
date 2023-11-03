from typing import Optional


class LogicGateError(Exception):
    ...


class LogicGate:
    def __init__(self):
        self._name: str = ""
        self._output_pin: Optional[int] = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def _logic(self) -> None:
        raise NotImplementedError("`_logic` needs to be implemented!")

    def get_output_pin(self) -> int:
        self._logic()
        return self._output_pin

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        raise NotImplementedError("`set_input_pin` needs to be implemented!")


class BinaryGate(LogicGate):
    def __init__(self):
        super(self, BinaryGate).__init__()
        self._input0_pin: Optional[int] = None
        self._input1_pin: Optional[int] = None

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        if pin == 0:
            if self._input0_pin is not None:
                raise LogicGateError("Input pin 0 has already been set!")
            else:
                self._input0_pin = value
        elif pin == 1:
            if self._input1_pin is not None:
                raise LogicGateError("Input pin 1 has already been set!")
            else:
                self._input1_pin = value
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")


class UnaryGate(LogicGate):
    def __init__(self):
        super(self, UnaryGate).__init__()
        self._input0_pin: Optional[int] = None

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        if pin == 0:
            if self._input0_pin is not None:
                raise LogicGateError("Input pin 0 has already been set!")
            else:
                self._input0_pin = value
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")
