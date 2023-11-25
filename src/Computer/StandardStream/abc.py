import abc

from Computer.Bit.abc import IBit, IBitString
from Computer.LogicCircuit.abc import IConnection

class IStdIn(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self, *, max_length: int):
        ...

    def feed(self) -> IBit:
        ...

    @abc.abstractclassmethod
    def set_input_value(self, *, value: IBit | IBitString, index: int) -> None:
        ...

    @abc.abstractclassmethod
    def set_output_connection(self, *, conn: IConnection) -> None:
        ...

class IStdOut(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def __init__(self):
        ...

    @abc.abstractclassmethod
    def print_output(self) -> None:
        ...

    @abc.abstractclassmethod
    def set_input_connection(self, *, conn: IConnection) -> None:
        ...