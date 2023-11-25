from typing import List

from .abc import IStdIn
from Computer.Bit import Bit, BitString
from Computer.Logger import OUT
from Computer.LogicCircuit.abc import IConnection

INFO = lambda msg: OUT.info(msg, level=7)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

class StdIn(IStdIn):
    
    def __init__(self, *, max_length: int):
        INFO("Creating a new standard input stream device.")

        self._output_connections: List[IConnection] = []
        self._stored_values: BitString = BitString(max_length=max_length)

    @property
    def stored_values(self) -> BitString:
        return self._stored_values
    
    def feed(self) -> None:
        INFO(f"Feeding {self._stored_values[0]} to the circuit.")
        return self._stored_values.pop_left()

    def set_input_value(self, *, value: Bit | BitString) -> None:
        if isinstance(value, Bit):
            INFO(f"Pushing {value} to the right side of the stored values.")
            self._stored_values.push_right(value)
        elif isinstance(value, BitString):
            INFO(
                f"Pushing bits: {[str(bit) for bit in value]} to the right of the "
                "stored values."
            )
            self._stored_values.extend_right(value)

    def set_output_connection(self, *, conn: IConnection) -> None:
        INFO("Connecting the wire to the standard input.")
        self._output_connections.append(conn)            
