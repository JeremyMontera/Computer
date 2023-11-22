from typing import List

from Computer.LogicCircuit.abc import ISwitch, IConnection
from Computer.LogicCircuit.Connection import ConnectionError
from Computer.LogicCircuit.LogicGate import LogicGateError
from Computer.Bit import Bit

ERROR = (ConnectionError, LogicGateError)

class SwitchError(Exception):
    ...

class Switch(ISwitch):
    
    def __init__(self):
        self._input_connections: List[IConnection] = [None, None]
        self._output_connection: IConnection = None

    def feed(self) -> Bit:
        if (
            not self.has_input_connection_set(index=0) and 
            not self.has_input_connection_set(index=1)
        ):
            raise SwitchError("The input connections have not all been set!")
        
        for conn in self._input_connections:
            try:
                return conn.feed()
            except ERROR:
                continue
        else:
            raise SwitchError("It looks like nothing is connected!")

    def has_input_connection_set(self, *, index: int) -> bool:
        if index not in list(range(len(self._input_connections))):
            raise SwitchError(f"You entered an unknown connection: {index}!")
        
        return self._input_connections[index] is not None

    def has_output_connection_set(self) -> bool:
        return self._output_connection is not None

    def reset(self) -> None:
        self._input_connections = [None, None]
        self._output_connection = None

    def set_input_connection(self, *, conn: IConnection, index: int) -> None:
        if self.has_input_connection_set(index=index):
            raise SwitchError(f"Input connection {index} has already been connected!")
        
        self._input_connections[index] = conn

    def set_output_connection(self, *, conn: IConnection) -> None:
        if self._output_connection is not None:
            raise SwitchError("The output connection has already been connected!")
        
        self._output_connection = conn