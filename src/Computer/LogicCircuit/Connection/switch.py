from typing import List, Optional

from Computer.Bit import Bit
from Computer.LogicCircuit.abc import IConnection, ISwitch
from Computer.LogicCircuit.Connection import ConnectionError
from Computer.LogicCircuit.LogicGate import LogicGateError

ERROR = (ConnectionError, LogicGateError)
# We need to be able to catch one of the switch's inputs hasn't been set yet - this
# might happen further upstream...


class SwitchError(Exception):
    """Handle any errors associated with the `Switch` class."""

    ...


class Switch(ISwitch):

    """
    This implements a 2-to-1 junction. The `Branch` class doesn't allow for this since
    normally you don't want multiple inputs feeding into the same output (it would
    cause serious electrical issues). This is a special case where we assume only one
    of the inputs will be set.

    TODO: extend this to a many-to-one relationship?

    Attributes:
        input_connections:  The inputs to the junction (private)
        output_connections: The output from the junction (private)
    """

    def __init__(self):
        """Constructor..."""

        self._input_connections: Optional[List[IConnection]] = [None, None]
        """
        The inputs to the junction:

        Type:
            List[Connection]
        """

        self._output_connection: Optional[IConnection] = None
        """
        The output from the junction.

        Type:
            Connection
        """

    def feed(self) -> Bit:
        """
        This is the primary method of this class. It will find the first input
        connection that is set, and will try calling its
        [`feed()`][Computer.LogicCircuit.Connection.Connection] method.

        TODO: should we check to see if all the connections were set, and yell at the
        user :/

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by the output device instead.

        Returns:
            information:
                The output of the device connected to this instance's input.
        """

        # Let's be smart and not shoot ourselves in the foot, please :)
        if not self.has_input_connection_set(
            index=0
        ) and not self.has_input_connection_set(index=1):
            raise SwitchError("The input connections have not all been set!")

        for conn in self._input_connections:
            try:
                return conn.feed()
            except ERROR:
                continue
        else:
            raise SwitchError("It looks like nothing is connected!")

    def has_input_connection_set(self, *, index: int) -> bool:
        """
        This method will check to see if there is a connection made to the input.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        # No shoot ourselves in the foot... it's late, what can I say?
        if index not in list(range(len(self._input_connections))):
            raise SwitchError(f"You entered an unknown connection: {index}!")

        return self._input_connections[index] is not None

    def has_output_connection_set(self) -> bool:
        """
        This method will check to see if there is an output connection.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return self._output_connection is not None

    def reset(self) -> None:
        """
        This method resets the input and output connections. This is mostly a
        convenience method to make testing smoother. It may not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.
        """

        self._input_connections = [None, None]
        self._output_connection = None

    def set_input_connection(self, *, conn: IConnection, index: int) -> None:
        """
        This will set an intput connection.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called within
            [`set_input_connection`][Computer.LogicCircuit.Connection.Connection] where
            an association relationship will be established.

        Args:
            conn:
                The connection we want to hook up to the inputs.
        """

        # For all that is good, please... don't shoot ourselves in the foot...
        if self.has_input_connection_set(index=index):
            raise SwitchError(f"Input connection {index} has already been connected!")

        self._input_connections[index] = conn

    def set_output_connection(self, *, conn: IConnection) -> None:
        """
        This will set an output connection.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called within
            [`set_input_connection`][Computer.LogicCircuit.Connection.Connection] where
            an association relationship will be established.

        Args:
            conn:
                The connection we want to hook up to the output.
        """

        # For all that is good, please... don't shoot ourselves in the foot...
        if self._output_connection is not None:
            raise SwitchError("The output connection has already been connected!")

        self._output_connection = conn
