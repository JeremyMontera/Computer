from typing import List, Optional

from Computer.Bit import Bit
from Computer.Logger import OUT
from Computer.LogicCircuit.abc import IBit, IConnection, ILoop

INFO = lambda msg: OUT.info(msg, level=6)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...


class LoopError(Exception):
    ...


class Loop(ILoop):

    """
    This class is a hack... since connecting the output of one gate to the output of
    another would cause an infinite loop (as it should in real life), this essentially
    mimics a connection loop - holding a value until the loop (connection 1) is
    accessed. The value in memory is initially set when you try to access the value in
    connection 0.

    Attributes:
        input_connection:   The input into the loop (private)
        output_connections: The outputs from the loop (private)
        memory:             The value that is stored in the loop (private)
    """

    def __init__(self):
        """Constructor..."""

        INFO("Creating a new empty loop connection.")

        self._input_connection: Optional[IConnection] = None
        """
        The input into the loop.

        Type:
            Optional[Connection]
        """

        self._output_connections: Optional[List[IConnection]] = [None, None]
        """
        The outputs from the loop.

        Type:
            Optional[List[Connection]]
        """

        self._memory: Optional[IBit] = None
        """
        The value that is stored in the loop.

        Type:
            Optional[Bit]
        """

    def feed(self, *, index: int) -> Bit:
        """
        This is the primary method of this class. It will check to see that a valid
        output connection has been set. It will then invoke that input conneciton's
        [`feed`][Computer.LogicCircuit.Connection.Connection] method. This will handle
        the two outputs differently:
            - Output 0: this is the output to the world, acts normally.
            - Output 1: this is the "loop", it is will return whatever is stored in the
                        memory.

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
                The output of the device connected to this instance's input or from the
                stored memory.
        """

        # Let's behave ourselves and not shoot ourselves in the foot.
        if index not in list(range(len(self._output_connections))):
            raise LoopError(f"You entered an unknown connection: {index}!")

        # Connection to the outside world
        if index == 0:
            # Like, OMG BECKY! Don't shoot ourselves in the foot, bitch.
            if not self.has_input_connection_set():
                raise LoopError("The input connection has not been set yet!")

            output: IBit = self._input_connection.feed()
            INFO(
                f"Feeding inforation {output} from outside the loop to the output "
                "connection."
            )

            # Save the memory, single went through and now should be circulated
            # indefinitly until the end of the program.
            if self._memory is None:
                INFO(f"The loop wasn't energized yet and now holds {output}.")
                self._memory = output

        # The "loop"
        elif index == 1:
            # Fucking hell, Becky, you dumb bitch. Don't shoot ourselves in the foot.
            if self._memory is None:
                raise LoopError("Looks like no signal came through yet!")

            output: IBit = self._memory
            INFO(
                f"Feeding infomation {output} held in the loop to the output "
                "connection."
            )

        return output

    def has_input_connection_set(self) -> bool:
        """
        This method will check to see if there is an input connection.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return self._input_connection is not None

    def has_output_connection_set(self, *, index: int) -> bool:
        """
        This method will check to see if there are any output connections.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        if index not in list(range(len(self._output_connections))):
            raise LoopError(f"You entered an unknown connection: {index}!")

        return self._output_connections[index] is not None

    def reset(self) -> None:
        """
        This method will reset all the input and output connections and delete the
        memory. This is mostly a convenience method to make testing smoother. It may
        not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.
        """

        INFO("Deactivating the loop and resetting the connections.")
        self._input_connection = None
        self._output_connections = [None, None]
        self._memory = None

    def set_input_connection(self, *, conn: IConnection) -> None:
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

        if self.has_input_connection_set():
            raise LoopError("The input connection has already been set!")

        INFO("Setting the input connection of the loop.")
        self._input_connection = conn

    def set_output_connection(self, *, conn: IConnection, index: int) -> None:
        """
        This will set one of the output connections.

        NOTE:
            This method is marked as public and can be called by the user, though it is
            more likely to be called within
            [`set_input_connection`][Computer.LogicCircuit.Connection.Connection] where
            an association relationship will be established.

        Args:
            conn:
                The connection we want to hook up to the outputs.
            index:
                Which output are we hooking up to?
        """

        if self.has_output_connection_set(index=index):
            raise LoopError(f"Output connection {index} is already connected!")

        if index == 0:
            INFO("Setting the outside connection of the loop.")
        elif index == 1:
            INFO("Setting the looping connection of the loop.")

        self._output_connections[index] = conn
