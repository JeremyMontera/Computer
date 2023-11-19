from typing import Optional, Dict

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.abc import IBranch

class Branch(IBranch):

    def __init__(self):
        ...

    def feed(self) -> Bit:
        ...

    def has_input_connection_set(self) -> bool:
        ...

    def has_mapping_set(self) -> bool:
        ...

    def has_output_connection_set(self) -> bool:
        ...

    def reset(self) -> None:
        ...

    def set_input_connection(self, conn: Optional[Connection] = None) -> None:
        ...

    def set_mapping(self, mapping: Dict[int, int]) -> None:
        ...

    def set_output_connection(self, conn: Optional[Connection] = None) -> None:
        ...

    