import abc
import enum
from typing import Optional, TypeVar

E = TypeVar("E", bound=enum.Enum)


class IConnection(metaclass=abc.ABCMeta):
    ...


class ILogicGate(metaclass=abc.ABCMeta):
    def __init__(self, type: Optional[E] = None, name: Optional[str] = None):
        ...

    def get_output_pin(self) -> int:
        ...

    def has_input_pin_set(self, pin: int = 0) -> bool:
        ...

    def reset(self) -> None:
        ...

    def set_input_pin(self, value: int | IConnection = 0, pin: int = 0) -> None:
        ...
