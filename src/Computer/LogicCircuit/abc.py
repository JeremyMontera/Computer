import abc
import enum
from typing import Literal, Optional, TypeVar

E = TypeVar('E', bound=enum.Enum)


class IConnection(metaclass=abc.ABCMeta):
    ...


class ILogicGate(metaclass=abc.ABCMeta):
    def __init__(self, type: Optional[E] = None, name: Optional[str] = None):
        ...

    def get_output_pin(self) -> int:
        ...

    def has_input_pin_set(self, pin: int) -> bool:
        ...

    def has_output_pin_set(self) -> bool:
        ...

    def reset(self) -> None:
        ...

    def set_input_pin(self, value: int | IConnection, pin: int) -> None:
        ...
