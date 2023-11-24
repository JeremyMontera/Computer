from typing import List

from .abc import IStdIn
from Computer.Bit import Bit, BitString
from Computer.Logger import OUT
from Computer.LogicCircuit.Connection import Connection

INFO = lambda msg: OUT.info(msg, level=8)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

class StdInError(Exception):
    ...


class StdIn(IStdIn):
    
    def __init__(self):
        INFO("Creating a new standard input stream device.")

        self._input_connections: List[Connection] = []
        self._value: BitString = BitString()

    def __iter__(self) -> Bit:
        for bit in self._value:
            yield bit

    @property
    def value(self) -> BitString:
        return self._value

    def set_input_connection(self, conn: Connection) -> None:
        if conn.has_input_connection_set():
            raise StdInError("The connection is already connected!")
        
        INFO("Connecting the wire to the standard input.")
        self._input_connections.append(conn)

    def set_input_value(self, value: Bit | BitString) -> None:
        if isinstance(value, Bit):
            self._value.push_right(value)
        elif isinstance(value, BitString):
            for bit in value:
                self._value.push_right(bit)
            
