from typing import TYPE_CHECKING, Optional

from Computer.LogicCircuit.abc import IConnection

if TYPE_CHECKING:
    from Computer.LogicCircuit.LogicGate import LogicGate


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

        self._input_connection: Optional["LogicGate"] = None
        """
        The device it receives data from.

        TODO: update when more devices implemented.

        Type:
            Optional[LogicGate]
        """

        self._output_connection: Optional["LogicGate"] = None
        """
        The device is feeds data to.

        TODO: update when more devices implemented.

        Type:
            Optional[LogicGate]
        """

    def feed(self) -> int:
        """
        This is the primary method of this class. It will check to see if the input has
        been set, and will try to get information from it. If it is a `LogicGate`
        instance, then it will try to call
        [`get_output_pin()`][Computer.LogicCircuit.LogicGate.get_output_pin].

        NOTE:
            This method is marked public and can be called by the user, though it is
            more likely to be called by the output device instead.

        TODO: need to handle other devices wires can be connected to.

        Returns:
            information:
                The output of the device connected to this instance's input.
        """

        # Yay! We don't want to shoot ourselves in the foot.
        if not self.has_input_connection_set():
            raise ConnectionError("The output connection has not been set yet!")

        # TODO: update this when we can connect to other things
        return self._input_connection.get_output_pin()

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

    def set_input_connection(self, gate: Optional["LogicGate"] = None) -> None:
        """
        This will set the input end of this instance. It will form an association
        relationship with the device by calling that device's set output and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        TODO: updated when we can connect to other devices.

        Args:
            gate:
                The device we want to connect to the input end of the wire.
        """

        # We no want to connect to nothing... and shoot ourselves in the foot...
        if gate is None:
            raise ConnectionError("You need to enter a gate to set the input!")

        # No good it is to shoot one's self in foot if already there be connection.
        if self.has_input_connection_set():
            raise ConnectionError("An input connection has already been made!")

        gate.set_output_pin(value=self)
        self._input_connection = gate

    def set_output_connection(
        self, gate: Optional["LogicGate"] = None, pin: int = 0
    ) -> None:
        """
        This will set the output end of this instance. It will form an association
        relationship with the device by calling that device's set input and pass this
        instance to the device.

        NOTE:
            This method is marked as public and can be called by the user.

        TODO: updated when we can connect to other devices. The function signature will
        need to be updated, so more than likely API-breaking change coming :(

        Args:
            gate:
                The device we want to connect to the input end of the wire.
            pin:
                Where to hook up the output end of the wire.
        """

        # We no want to connect to nothing... and shoot ourselves in the foot...
        if gate is None:
            raise ConnectionError("You need to enter a gate to set the output!")

        # No good it is to shoot one's self in foot if already there be connection.
        if self.has_output_connection_set():
            raise ConnectionError("An output connection has already been made!")

        gate.set_input_pin(value=self, pin=pin)
        self._output_connection = gate
