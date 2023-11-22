from typing import Optional, Tuple

from Computer.Bit import Bit
from Computer.LogicCircuit.abc import IBranch, IConnection, ILogicGate

DEVICE = ILogicGate | Tuple[IBranch, int]
# This represents an arbitrary device the wire can be connected to.
# NOTE: right now, for `Branch` objects, we need to also save this instance's position
# in `Branch._output_connections` array so that we can get the right input connection.


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

        self._input_connection: Optional[DEVICE] = None
        """
        The device it receives data from.

        Type:
            Optional[LogicGate | Branch]
        """

        self._output_connection: Optional[DEVICE] = None
        """
        The device is feeds data to.

        Type:
            Optional[LogicGate | Branch]
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
            return self._input_connection.get_output_pin()
        elif isinstance(self._input_connection, tuple):
            return self._input_connection[0].feed(index=self._input_connection[1]-1)

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

        self._input_connection = None
        self._output_connection = None

    def set_input_connection(self, *, device: DEVICE) -> None:
        """
        This will set the input end of this instance. It will form an association
        relationship with the device by calling that device's set output and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            device:
                The device we want to connect to the input end of the wire.
        """

        if isinstance(device, ILogicGate):
            # No good it is to shoot one's self in foot if already there be connection.
            if self.has_input_connection_set():
                raise ConnectionError("An input connection has already been made!")

            device.set_output_pin(value=self)

        elif isinstance(device, IBranch):
            device.set_output_connection(conn=self)
            device = (device, device.num_output_connections)

        self._input_connection = device

    def set_output_connection(self, *, device: DEVICE, pin: int) -> None:
        """
        This will set the output end of this instance. It will form an association
        relationship with the device by calling that device's set input and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        Args:
            device:
                The device we want to connect to the input end of the wire.
            pin:
                Where to hook up the output end of the wire.
        """

        if isinstance(device, ILogicGate):
            # No good it is to shoot one's self in foot if already there be connection.
            if self.has_output_connection_set():
                raise ConnectionError("An output connection has already been made!")

            device.set_input_pin(value=self, pin=pin)

        elif isinstance(device, IBranch):
            device.set_input_connection(conn=self)
            device = (device, device.num_input_connections)

        self._output_connection = device
