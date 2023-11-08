from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Computer.LogicGate import LogicGate


class ConnectionError(Exception):
    ...


class Connection:

    """
    This will implement a connection between logic gates. It is essentially a wire that
    has a bandwidth of one bit currently. It can read bits in serial one at a time. The
    user is expected to be able to make the connections between components with logic
    gates and that is it. The user is not expected to have to feed the bits from one
    gate to the other.

    Attributes:
        input_connection:   the logic gate connection is receiving data from (private)
        output_connection:  the logic gate connection is feeding data to (private)
    """

    def __init__(self):
        """Constructor..."""

        self._input_connection: Optional["LogicGate"] = None
        """
        The logic gate the connection is receiving data from.

        Type:
            LogicGate
        """
        
        self._output_connection: Optional["LogicGate"] = None
        """
        The logic gate the connection is feed data to.

        Type:
            LogicGate
        """

    def feed(self) -> int:
        """
        This will take the value of the output pin of the gate connected to the input
        and return it.

        While this is a public method, the user is not expected to call this method
        directly. Instead, when trying to get the output of the last gate, it will
        attempt to call this method to get data from the gates higher up the chain:

        Sequence of events - given AndGate -> NotGate:
            (1) NotGate.get_output_pin() calls
            (2) NotGate._logic() calls
            (3) NotGate._input0_pin.feed() calls
            (4) AndGate.get_output_pin() calls
            (5) AndGate._logic() ...

        Returns:
            data:
                ...
        """

        if self._input_connection is None:
            raise ConnectionError("The output hasn't been connected yet!")

        print(f"[00:00:00] Feeding input gate {self._input_connection.name}'s output.")
        return self._input_connection.get_output_pin()

    def set_input_connection(self, gate: "LogicGate") -> None:
        """
        This will set the input of the wire to the output of the requested gate. This
        will form a aggregation relationship: the connection has-a gate.

        This is a public method and is intended to be called by the user and will
        update the internal state of the `Connection` instance.

        Example:
            ```python
            >>> gate = AndGate()
            >>> conn = Connection()
            >>> gate.name = "and gate"
            >>> conn.set_input_connection(gate)
            [00:00:00] Setting and gate's output pin to the input connection.
            ```

        Args:
            gate:
                ...
        """

        if gate.has_output_pin_set():
            raise ConnectionError(f"{gate.name}'s output pin is already set!")

        print(f"[00:00:00] Setting {gate.name}'s output pin to the input connection.")
        self._input_connection = gate

    def set_output_connection(self, gate: "LogicGate", pin: int = 0) -> None:
        """
        This will set the output of the wire to the input of the requested gate. This
        will form a aggregation relationship: the connection has-a gate.

        This is a public method and is intended to be called by the user and will
        update the internal state of the `Connection` instance.

        Example:
            ```python
            >>> gate = AndGate()
            >>> gate.name = "and gate"
            >>> conn.set_output_connection(gate)
            [00:00:00] Setting and gate's input pin to the output connection.
            [00:00:00] The input has been validated.
            [00:00:00] Setting the input for pin 0.
            ```

        Args:
            gate:
                ...
            pin:
                (Optional) which pin to set the connection to. This is optional to
                handle unary gates.
        """

        if gate.has_input_pin_set(pin=pin):
            raise ConnectionError(f"{gate.name} already has pin {pin} set!")

        print(f"[00:00:00] Setting {gate.name}'s input pin to the output connection.")
        gate.set_input_pin(self, pin=pin)
        self._output_connection = gate
