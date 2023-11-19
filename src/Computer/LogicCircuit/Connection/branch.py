from typing import List, Optional, Dict

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.abc import IBranch


class BranchError(Exception):
    ...


class Branch(IBranch):
    def __init__(self):
        self._input_connections: List[Connection] = []
        self._mapping: Dict[int, int] = None
        self._output_connections: List[Connection] = []

    def _validate_mapping(self, mapping: Dict[int, int]) -> None:
        inputs: List[int] = list(set(mapping.values()))
        outputs: List[int] = list(mapping.keys())
        
        inputs.sort()
        outputs.sort()

        assert inputs == list(
            range(len(self._input_connections))
        ), "Not all of the outputs are connected to inputs!"
        assert outputs == list(
            range(len(self._output_connections))
        ), "Not all of the outputs have connections!"

    def feed(self) -> Bit:
        ...

    def has_input_connection_set(self) -> bool:
        return len(self._input_connections) > 0

    def has_mapping_set(self) -> bool:
        return self._mapping is not None

    def has_output_connection_set(self) -> bool:
        return len(self._output_connections) > 0

    def reset(self) -> None:
        self._input_connections = []
        self._output_connections = []
        self._mapping = None

    def set_input_connection(self, conn: Optional[Connection] = None) -> None:
        if self._mapping is not None:
            raise BranchError(
                "The mapping has been set already! "
                "You cannot add any more connections!"
            )

        if conn is None:
            raise BranchError("You need to enter a connection!")

        self._input_connections.append(conn)

    def set_mapping(self, mapping: Optional[Dict[int, int]] = None) -> None:
        if mapping is None:
            raise BranchError("You need to enter a valid mapping!")

        if self._mapping is not None:
            raise BranchError("The mapping has been set already!")

        self._validate_mapping(mapping)
        self._mapping = mapping

    def set_output_connection(self, conn: Optional[Connection] = None) -> None:
        if self._mapping is not None:
            raise BranchError(
                "The mapping has been set already! "
                "You cannot add any more connections!"
            )

        if conn is None:
            raise BranchError("You need to enter a connection!")

        self._output_connections.append(conn)
