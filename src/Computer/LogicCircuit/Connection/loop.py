from typing import Optional, List

from Computer.LogicCircuit.abc import ILoop, IConnection, IBit
from Computer.Bit import Bit

class LoopError(Exception):
    ...

class Loop(ILoop):
    
    def __init__(self):
        self._input_connection: Optional[IConnection] = None
        self._output_connections: Optional[List[IConnection]] = [None, None]
        self._memory: Optional[IBit] = None

    def feed(self, *, index: int) -> Bit:
        if index not in list(range(len(self._output_connections))):
            raise LoopError(f"You entered an unknown connection: {index}!")
        
        if index == 0:
            if not self.has_input_connection_set():
                raise LoopError("The input connection has not been set yet!")
        
            output: IBit = self._input_connection.feed()
            if self._memory is None:
                self._memory = output

        elif index == 1:
            if self._memory is None:
                raise LoopError("Looks like no signal came through yet!")
            
            output: IBit = self._memory

        return output

    def has_input_connection_set(self) -> bool:
        return self._input_connection is not None

    def has_output_connection_set(self, *, index: int) -> bool:
        if index not in list(range(len(self._output_connections))):
            raise LoopError(f"You entered an unknown connection: {index}!")
        
        return self._output_connections[index] is not None

    def reset(self) -> None:
        self._input_connection = None
        self._output_connections = [None, None]
        self._memory = None

    def set_input_connection(self, *, conn: IConnection) -> None:
        if self.has_input_connection_set():
            raise LoopError("The input connection has already been set!")
        
        self._input_connection = conn

    def set_output_connection(self, *, conn: IConnection, index: int) -> None:
        if self.has_output_connection_set(index=index):
            raise LoopError(f"Output connection {index} is already connected!")
        
        self._output_connections[index] = conn