from __future__ import annotations

import abc
import enum
from typing import Optional, TypeVar

E = TypeVar("E", bound=enum.Enum)


class IConnection(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self):
        ...

    @abc.abstractclassmethod
    def feed(self) -> int:
        ...

    @abc.abstractclassmethod
    def has_input_connection_set(self) -> bool:
        ...

    @abc.abstractclassmethod
    def has_output_connection_set(self) -> bool:
        ...

    @abc.abstractclassmethod
    def reset(self) -> None:
        ...

    @abc.abstractclassmethod
    def set_input_connection(self, gate: Optional[ILogicGate] = None) -> None:
        ...

    @abc.abstractclassmethod
    def set_output_connection(self, gate: Optional[ILogicGate] = None) -> None:
        ...


class ILogicGate(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self, type: Optional[E] = None, name: Optional[str] = None):
        ...

    @abc.abstractclassmethod
    def get_output_pin(self) -> int:
        ...

    @abc.abstractclassmethod
    def has_input_pin_set(self, pin: int = 0) -> bool:
        ...

    @abc.abstractclassmethod
    def has_output_pin_set(self) -> bool:
        ...

    @abc.abstractclassmethod
    def reset(self) -> None:
        ...

    @abc.abstractclassmethod
    def set_input_pin(self, value: int | IConnection = 0, pin: int = 0) -> None:
        ...

    @abc.abstractclassmethod
    def set_output_pin(self, value: Optional[IConnection] = None) -> None:
        ...
