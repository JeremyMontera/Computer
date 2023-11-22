from typing import Dict, List

from Computer.Bit import Bit
from Computer.LogicCircuit.abc import IBranch, IConnection


class BranchError(Exception):
    """Handle any errors associated with the `Branch` class."""

    ...


class Branch(IBranch):

    """
    This implements a branching connection: multiple wires comming in and multiple
    wires going out of a single junction. This will keep track of which outputs are
    connected to which inputs, with the assumption that the mapping is at least
    surjective.

    Attributes:
        input_connections:  The inputs into the branch (private)
        mapping:            The mapping of output to input connections (private)
        output_connections: The outputs leaving the branch (private)
    """

    def __init__(self):
        """Constructor..."""

        self._input_connections: List[IConnection] = []
        """
        The inputs into the branch.

        Type:
            List[Connection]
        """

        self._mapping: Dict[int, int] = None
        """
        The mapping of output to input connections.

        Type:
            Optional[Dict[int, int]]
        """

        self._output_connections: List[IConnection] = []
        """
        The outputs leaving the branch.

        Type:
            List[Connection]
        """

    @property
    def num_input_connections(self) -> int:
        """Read the length of the `input_connections` list."""

        return len(self._input_connections)

    @property
    def num_output_connections(self) -> int:
        """Read the length of the `output_connections` list."""

        return len(self._output_connections)

    def _validate_mapping(self, mapping: Dict[int, int]) -> None:
        """
        This validates the mapping from outputs to inputs. This will check if the
        mapping is surjective: it will check if all the input and output connections
        have a mapping, but not how many mappings to one input there are.

        This is a private method.

        Args:
            mapping:
                The mapping of output to input connections.
        """
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

    def feed(self, *, index: int) -> Bit:
        """
        This is the primary method of this class. It will check to see that a valid
        output connection has been set. It will then invoke that input conneciton's
        [`feed`][Computer.LogicCircuit.Connection.Connection] method.

        TODO: can this be implemented cleaner? Passing `index` seems like a work-around
        since we need to know which output connection called this feed method.

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by the output connection instead.

        Args:
            index:
                Who called this method.

        Returns:
            information:
                The output of the device connected to this instance's input.
        """

        # For the love of god, don't shoot ourselves in the foot.
        if index not in list(range(len(self._output_connections))):
            raise BranchError(f"{index} doesn't correspond to any output connection!")

        return self._input_connections[self._mapping[index]].feed()

    def has_input_connection_set(self) -> bool:
        """
        This method will check to see if there are any input connections.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return len(self._input_connections) > 0

    def has_mapping_set(self) -> bool:
        """
        This method will check to see if the mapping has been set yet.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return self._mapping is not None

    def has_output_connection_set(self) -> bool:
        """
        This method will check to see if there are any output connections.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return len(self._output_connections) > 0

    def reset(self) -> None:
        """
        This method will reset all the input and output connections and delete the
        mapping. This is mostly a convenience method to make testing smoother. It may
        not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.
        """

        self._input_connections = []
        self._output_connections = []
        self._mapping = None

    def set_input_connection(self, *, conn: IConnection) -> None:
        """
        This will set an intput connection assuming no mapping has been set yet.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called within
            [`set_input_connection`][Computer.LogicCircuit.Connection.Connection] where
            an association relationship will be established.

        Args:
            conn:
                The connection we want to hook up to the inputs.
        """

        if self._mapping is not None:
            raise BranchError(
                "The mapping has been set already! "
                "You cannot add any more connections!"
            )

        self._input_connections.append(conn)

    def set_mapping(self, *, mapping: Dict[int, int]) -> None:
        """
        This will establish a mapping between outputs and inputs. After the mapping has
        been set, no other inputs or outputs can be connected.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            mapping:
                The mapping of output to input connections.
        """

        if self._mapping is not None:
            raise BranchError("The mapping has been set already!")

        self._validate_mapping(mapping)
        self._mapping = mapping

    def set_output_connection(self, *, conn: IConnection) -> None:
        """
        This will set an output connection assuming no mapping has been set yet.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called within
            [`set_input_connection`][Computer.LogicCircuit.Connection.Connection] where
            an association relationship will be established.

        Args:
            conn:
                The connection we want to hook up to the inputs.
        """

        if self._mapping is not None:
            raise BranchError(
                "The mapping has been set already! "
                "You cannot add any more connections!"
            )

        self._output_connections.append(conn)
