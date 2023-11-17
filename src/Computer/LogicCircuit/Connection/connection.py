from typing import TYPE_CHECKING, Optional
from Computer.LogicCircuit.abc import IConnection

if TYPE_CHECKING:
    from Computer.LogicCircuit.LogicGate import LogicGate


class ConnectionError(Exception):
    ...


class Connection(IConnection):

    def __init__(self):
        self._input_connection: Optional["LogicGate"] = None
        self._output_connection: Optional["LogicGate"] = None

    def feed(self) -> int:
        if not self.has_output_connection_set():
            raise ConnectionError(f"The output connection has not been set yet!")
        
        # TODO: update this when we can connect to other things
        return self._output_connection.get_output_pin()
    
    def has_input_connection_set(self) -> bool:
        return self._input_connection is not None

    def has_output_connection_set(self) -> bool:
        return self._output_connection is not None

    def reset(self) -> None:
        self._input_connection = None
        self._output_connection = None

    def set_input_connection(self, gate: Optional['LogicGate'] = None) -> None:
        if gate is None:
            raise ConnectionError("You need to enter a gate to set the input!")
        
        if self.has_input_connection_set():
            raise ConnectionError("An input connection has already been made!")
        
        if gate.has_output_pin_set():
            raise ConnectionError(f"{gate.name} already is connected!")
        
        self._input_connection = gate

    def set_output_connection():
        ...
