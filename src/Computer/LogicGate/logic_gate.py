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
    
    def _sanitize_input(self, value: int) -> None:
        assert value == 0 or value == 1, f"{value} is not a valid input!"

    def get_output_pin(self) -> int:
        self._logic()
        return self._output_pin

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        raise NotImplementedError("`set_input_pin` needs to be implemented!")
