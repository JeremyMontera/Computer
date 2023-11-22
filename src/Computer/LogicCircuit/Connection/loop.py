from Computer.LogicCircuit.abc import ILoop
from Computer.Bit import Bit

class LoopError(Exception):
    ...

class Loop(ILoop):
    
    def __init__(self):
        ...

    def feed(self) -> Bit:
        ...

    def has_input_connection_set(self) -> bool:
        ...

    def has_output_connection_set(self) -> bool:
        ...

    def reset(self) -> None:
        ...

    def set_input_connection(self) -> None:
        ...

    def set_output_connection(self) -> None:
        ...