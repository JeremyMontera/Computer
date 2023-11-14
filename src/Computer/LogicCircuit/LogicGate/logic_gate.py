import enum
from typing import Optional, Union, List, cast
from Computer.LogicCircuit import abc
from Computer.LogicCircuit.Connection import Connection

PIN = Union[int, 'Connection']


class LogicType(enum.Enum):
    NOT: int = 1
    AND: int = 2
    OR: int = 2


class LogicGateError(Exception):
    ...


class LogicGate(abc.ILogicGate):
    
    def __init__(self, type: Optional[LogicType] = None, name: Optional[str] = None):
        if type is None:
            raise LogicGateError("You need to pass a valid logic gate type!")
        
        self._type: LogicType = type
        self._name: str = "" if name is None else name
        self._output_pin: Optional[PIN] = cast(PIN, None)
        self._input_pins: List[Optional[PIN]] = [cast(PIN, None)] * self._type.value

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def type(self) -> LogicType:
        return self._type
    
    def _logic(self) -> None:
        inputs: List[int] = [None] * self._type.value
        for p, pin in enumerate(self._input_pins):
            if pin is None:
                raise LogicGateError(f"Pin {p} has not been set yet!")
            elif isinstance(pin, Connection):
                inputs[p] = pin.feed()
            elif isinstance(pin, int):
                inputs[p] = pin

        if self._type == LogicType.NOT:
            output: bool = not bool(inputs[0])
        elif self._type == LogicType.AND:
            output: bool = bool(inputs[0]) and bool(inputs[1])
        elif self._type == LogicType.OR:
            output: bool = bool(inputs[0]) or bool(inputs[1])

        self._output_pin = int(output)

    def _sanitize_input(self, value: int | 'Connection') -> None:
        if isinstance(value, int):
            assert value in [0, 1], f"{value} is not a valid input!"
    
    def get_output_pin(self) -> int:
        if self._output_pin is None:
            self._logic()

        return self._output_pin
    
    def has_input_pin_set(self, pin: int) -> bool:
        if pin not in list(range(len(self._input_pins))):
            raise LogicGateError(f"Entered an invalid pin: {pin}!")
        
        return self._input_pins[pin] is not None
    
    def has_output_pin_set(self) -> bool:
        return self._output_pin is not None
    
    def set_input_pin(self, value: int | 'Connection', pin: int) -> None:
        self._sanitize_input(pin)
        if self.has_input_pin_set(pin):
            raise LogicGateError(f"Input pin {pin} has already been set!")
        
        self._input_pins[pin] = value
    
    def reset(self) -> None:
        self._input_pins = [None] * self._type.value
        self._output_pin = None
