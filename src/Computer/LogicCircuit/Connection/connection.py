from typing import Optional, Tuple

from Computer.Bit import Bit
from Computer.Logger import OUT
from Computer.LogicCircuit.abc import (IBranch, IConnection, ILogicGate, ILoop,
                                       ISwitch)
from Computer.StandardStream.abc import IStdIn, IStdOut

INFO = lambda msg: OUT.info(msg, level=3)  # noqa: E731
# Short-cut so we don't have to keep writing the same stuff...

DEVICE = (
    ILogicGate | IBranch | Tuple[IBranch, int] | ISwitch | ILoop | Tuple[ILoop, int] | IStdIn | IStdOut
)
# This represents an arbitrary device the wire can be connected to.
# NOTE: right now, for `Branch` objects, we need to also save this instance's position
# in `Branch._output_connections` array so that we can get the right input connection.
# NOTE: same thing with `Loop` objects, just now the output connection.


class ConnectionError(Exception):
    """Handle any errors associated with the `Connection` class."""

    ...


class Connection(IConnection):

    """
    This implements a wire connecting two other devices. This is done via the
    aggregation relationship. When data is requested, it will feed information from the
    input to the output.

    Attributes:
        input_connection:   The device it receives data from (private)
        output_connection:  The device it feeds data to (private)
    """

    def __init__(self):
        """Constructor..."""

        INFO("Creating a new empty wire.")

        self._input_connection: Optional[DEVICE] = None
        """
        The device it receives data from.

        Type:
            Optional[LogicGate | Branch | Switch | Loop]
        """

        self._output_connection: Optional[DEVICE] = None
        """
        The device is feeds data to.

        Type:
            Optional[LogicGate | Branch | Switch | Loop]
        """

    def feed(self) -> Bit:
        """
        This is the primary method of this class. It will check to see if the input has
        been set, and will try to get information from it. If it is a `LogicGate`
        instance, then it will try to call
        [`get_output_pin()`][Computer.LogicCircuit.LogicGate.get_output_pin].

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by the output device instead.

        Returns:
            information:
                The output of the device connected to this instance's input.
        """

        # Yay! We don't want to shoot ourselves in the foot.
        if not self.has_input_connection_set():
            raise ConnectionError("The output connection has not been set yet!")

        if isinstance(self._input_connection, ILogicGate):
            output: Bit = self._input_connection.get_output_pin()
        elif isinstance(self._input_connection, tuple):
            output: Bit = self._input_connection[0].feed(
                index=self._input_connection[1]
            )
        elif isinstance(self._input_connection, ISwitch) or isinstance(self._input_connection, IStdIn):
            output: Bit = self._input_connection.feed()

        INFO(f"Feeding information {output} to the output device.")
        return output

    def has_input_connection_set(self) -> bool:
        """
        This method will check to see if there is a device connected to the input of
        this instance.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return self._input_connection is not None

    def has_output_connection_set(self) -> bool:
        """
        This method will check to see if there is a device connected to the output of
        this instance.

        NOTE:
            This method is marked public and can be called by the user.

        Returns:
            flag:
                ...
        """

        return self._output_connection is not None

    def reset(self) -> None:
        """
        This method reset the input and output ends of the wire. This is mostly a
        convenience method to make testing smoother. It may not exist forever.

        NOTE:
            This method is marked as public and can be called by the user.
        """

        INFO("Resetting the wire's connections.")
        self._input_connection = None
        self._output_connection = None

    def set_input_connection(self, *, device: DEVICE, index: Optional[int] = 0) -> None:
        """
        This will set the input end of this instance. It will form an association
        relationship with the device by calling that device's set output and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            device:
                The device we want to connect to the input end of the wire.
            index:
                Which location on the device the input connection of the wire should
                be connected to.
        """

        # No good it is to shoot one's self in foot if already there be connection.
        if self.has_input_connection_set():
            raise ConnectionError("An input connection has already been made!")

        INFO(
            "Attempting to hook the wire's input connection to the device's output "
            "connection."
        )

        if isinstance(device, ILogicGate):
            if device.has_output_pin_set():
                raise ConnectionError(f"{device.name}'s output is already connected!")

            device.set_output_pin(value=self)

        elif isinstance(device, IBranch):
            device.set_output_connection(conn=self)
            device = (device, device.num_output_connections - 1)

        elif isinstance(device, ISwitch):
            if device.has_output_connection_set():
                raise ConnectionError("This switch is already fully connected!")

            device.set_output_connection(conn=self)

        elif isinstance(device, ILoop):
            if device.has_output_connection_set(index=index):
                raise ConnectionError(
                    f"Output connection {index} of this loop is already connected!"
                )

            device.set_output_connection(conn=self, index=index)
            device = (device, index)

        elif isinstance(device, IStdIn):
            device.set_output_connection(conn=self)

        self._input_connection = device

    def set_output_connection(self, *, device: DEVICE, index: int) -> None:
        """
        This will set the output end of this instance. It will form an association
        relationship with the device by calling that device's set input and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            device:
                The device we want to connect to the input end of the wire.
            index:
                Where to hook up the output end of the wire.
        """

        # No good it is to shoot one's self in foot if already there be connection.
        if self.has_output_connection_set():
            raise ConnectionError("An output connection has already been made!")

        INFO(
            "Attempting to set the wire's output connection to the device's input "
            "connection."
        )

        if isinstance(device, ILogicGate):
            if device.has_input_pin_set(pin=index):
                raise ConnectionError(f"{device.name}'s input is already connected!")

            device.set_input_pin(value=self, pin=index)

        elif isinstance(device, IBranch):
            device.set_input_connection(conn=self)
            device = (device, device.num_input_connections)

        elif isinstance(device, ISwitch):
            if device.has_input_connection_set(index=index):
                raise ConnectionError("This switch is already fully connected!")

            device.set_input_connection(conn=self, index=index)

        elif isinstance(device, ILoop):
            if device.has_input_connection_set():
                raise ConnectionError("This loop is already connected!")

            device.set_input_connection(conn=self)

        elif isinstance(device, IStdOut):
            device.set_input_connection(conn=self)

        self._output_connection = device
