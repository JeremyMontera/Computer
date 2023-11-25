from typing import List

from .abc import IStdOut
from Computer.Bit import Bit
from Computer.LogicCircuit.abc import IConnection
from Computer.Logger import OUT

INFO = lambda msg: OUT.info(msg, level=8)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

class StdOut(IStdOut):
    
    def __init__(self):
        INFO("Creating a new standard output stream device!")
        self._input_connections: List[IConnection] = []

    def print_output(self) -> None:
        INFO("Printing the output of the circuit.")
        for c, conn in enumerate(self._input_connections):
            output: Bit = conn.feed()
            INFO(f"\tOutput {c}: {str(output)}")

    def set_input_connection(self, *, conn: IConnection) -> None:
        INFO("Connecting the wire to the standard output.")
        self._input_connections.append(conn)