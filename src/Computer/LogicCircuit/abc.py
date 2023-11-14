import abc
from typing import Generic, Optional

T = Generic('T')

class ILogicGate(metaclass=abc.ABCMeta):

    def __init__(self, type: Optional[T] = None, name: Optional[str] = None):
        ...

    def get_output_pin(self) -> int:
        ...

    def has_input_pin_set(self, pin: T) -> bool:
        ...

    def has_output_pin_set(self) -> bool:
        ...

    def reset(self) -> None:
        ...

    def set_input_pin(self, pin: T) -> None:
        ...