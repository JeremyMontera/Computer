from typing import List

from .abc import IStdIn
from Computer.Bit import Bit, BitString
from Computer.Logger import OUT
from Computer.LogicCircuit.Connection import Connection

INFO = lambda msg: OUT.info(msg, level=7)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

class StdInError(Exception):
    ...


class StdIn(IStdIn):
    
    def __init__(self, *, max_length: int):
        INFO("Creating a new standard input stream device.")

        self._input_connections: List[Connection] = []
        self._stored_values: BitString = BitString(max_length=max_length)

    @property
    def stored_values(self) -> BitString:
        return self._stored_values
    
    def feed(self) -> None:
        return self._stored_values.pop_left()

    def set_input_connection(self, *, conn: Connection) -> None:
        if conn.has_input_connection_set():
            raise StdInError("The connection is already connected!")
        
        INFO("Connecting the wire to the standard input.")
        self._input_connections.append(conn)

    def set_input_value(self, *, value: Bit | BitString) -> None:
        if isinstance(value, Bit):
            self._stored_values.push_right(value)
        elif isinstance(value, BitString):
            self._stored_values.extend_right(value)
            
