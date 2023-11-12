from typing import List, Optional, Union

from Computer.LogicCircuit.Connection import Connection

from .logic_gate import ILogicGate, LogicGateError

PIN = Optional[Union[int, 'Connection']]


class OrGate(ILogicGate):

    """
    This implements an or gate. This "is a" type of binary gate. This will implement
    the logic of the Boolean `'or'` operation. It will inherit all of the attributes
    and behaviors of the `BinaryGate` parent class.

    Attributes:
        input_pins:     the list of all possible input pins (private)
        name:           the name of the logic gate (public)
        output_pin:     the output pin (private)
    """

    def __init__(self):
        """Constructor..."""

        self._input_pins: List[PIN] = [None, None]
        """
        The list of all possible input pins.

        Type:
            List[int | Connection]
        """

        self._name: str = ""
        """
        The name of the logic gate.

        Type:
            string
        """

        self._output_pin: PIN = None
        """
        The output pin.

        Type:
            integer | Connection
        """

    @property
    def name(self) -> str:
        """The name of the logic gate."""

        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the logic gate."""

        self._name = value

    def _logic(self) -> None:
        """
        This implements the logic of the Boolean `'or'` operation. It takes the value
        of the two input pins and will set the resulting value to the output pin.

            pin0 | pin1 | output
            --------------------
              0  |  0   |    0
              0  |  1   |    1
              1  |  0   |    1
              1  |  1   |    1

        This is a private method not intended to be directly called by the user.

        Raises:
            LogicGateError:
                (1) The first input pin has not been set!
                (2) The second input pin has not been set!
        """

        for p in range(len(self._input_pins)):
            if self._input_pins[p] is None:
                raise LogicGateError(f"Input pin {p} has not been set!")

        inputs: List[Union[int, Connection]] = [None, None]
        for p in range(len(self._input_pins)):
            if isinstance(self._input_pins[p], Connection):
                inputs[p] = self._input_pins[p].feed()
            elif isinstance(self._input_pins[p], int):
                inputs[p] = self._input_pins[p]

        output = bool(inputs[0]) or bool(inputs[1])

        print(f"[00:00:00] {bool(inputs[0])} or {bool(inputs[1])} is {output}.")

        self._output_pin = int(output)

    def _sanitize_input(self, value: Union[int, "Connection"]) -> None:
        """
        This will check the values being set to the input pins. Since inputs are
        assumed to be binary, it checks if the input is 0/1. This is called when
        `set_input_pin` is called by one of the descendants.

        This is a private method not intended to be directly called by the user.

        Raises:
            {value} is not a valid input!

        Args:
            value:
                The value to be inputted to the logic gate.
        """

        if isinstance(value, int):
            assert value == 0 or value == 1, f"{value} is not a valid input!"

        print("[00:00:00] The input has been validated.")

    def get_output_pin(self) -> int:
        """
        This will get the value of the output pin. This will first run the logic of the
        logic gate to compute the output. Since `_logic` is assumed to be private, and
        `_output_pin` is private, it is assumed that the user will not have been able
        to set the value of the output. However, it will bypass this `_logic` call if
        `_output_pin` is not `'None'`.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an output that has
        this method implemented for polymorphism.

        Returns:
            output_pin:
                The value of the output after the logic has been applied to the values
                held by the input pins.
        """

        if self._output_pin is None:
            print("[00:00:00] The output pin has not been set yet.")

            self._logic()

        print("[00:00:00] Getting the output of the gate.")

        return self._output_pin
    
    def has_input_pin_set(self, pin: Optional[int] = 0) -> bool:
        """
        This will check to see if the requested input pin has been set yet.

        This is a public method that can be called by the user, but more than likely,
        it will be called by the `Connection` class.

        Args:
            pin:
                (Optional) The pin to check. This defaults to pin 0.

        Returns:
            flag:
                ...
        """

        try:
            return self._input_pins[pin] is not None
        except IndexError:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")
        
    def has_output_pin_set(self) -> bool:
        """
        This will check to see if the output pin has been set yet. Most of the time,
        the expectation is that this is not set.

        This is a public method that can be called by the user, but more than likely,
        it will be called by the `Connection` class.

        Returns:
            flag:
                ...
        """

        return self._output_pin is not None
    
    def set_input_pin(self, value: Union[int, "Connection"], pin: int = 0) -> None:
        """
        This will set the input pins.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an input that has
        this method implemented for polymorphism.

        Args:
            value:
                The value to set the pin to.
            pin:
                (Optional) the pin to set the value to. This defaults to zero to
                handle the case of unary gates.
        """

        self._sanitize_input(value)
        if self.has_input_pin_set(pin=pin):
            raise LogicGateError(f"Input pin {pin} has already been set!")
        else:
            print(f"[00:00:00] Setting the input for pin {pin}.")
            self._input_pins[pin] = value
