from typing import Optional

from .logic_gate import LogicGate, LogicGateError


class BinaryGate(LogicGate):

    """
    This implements a binary gate class (i.e., it assumes two inputs). This "is a" type
    of `LogicGate` and so will inherit attributes/behaviors from said `LogicGate`
    class. However, the logic will be deferred to specific child classes of this class.

    Attributes:
        input0_pin:     the first input pin (private)
        input1_pin:     the second input pin (private)
        name:           the name of the logic gate class (public)
        output_pin:     the output of the pin that set later on by the logic (private)
    """

    def __init__(self):
        """Constructor..."""

        super().__init__()
        """
        This inherits from the `LogicGate` parent class.
        """

        self._input0_pin: Optional[int] = None
        """
        The first input pin of the binary gate. This is initially set to `'None'`.

        TODO: see the TODO under `_output_pin` in `LogicGate` class.

        Type:
            integer
        """

        self._input1_pin: Optional[int] = None
        """
        The second input pin of the binary gate. This is initially set to `'None'`.

        TODO: see the TODO under `_output_pin` in `LogicGate` class.

        Type:
            integer
        """

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        """
        This will set the input pins. It will allow the user to set the value of either
        of the two pins.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an input that has
        this method implemented for polymorphism.

        Example:
            ```python
            >>> or_gate = OrGate()
            >>> or_gate.set_input_pin(1, pin=0)
            [00:00:00] The input has been validated.
            [00:00:00] Setting the input for pin 0.
            ```

        Raises:
            LogicGateError:
                (1) Input pin 0 has already been set!
                (2) Input pin 1 has already been set!
                (3) Entered an unknown pin: {pin}!

        Args:
            value:
                The value to set the pin to.
            pin:
                (Optional) the pin to set the value to. This defaults to zero to
                handle the case of unary gates.
        """

        self._sanitize_input(value)
        if pin == 0:
            if self._input0_pin is not None:
                raise LogicGateError("Input pin 0 has already been set!")
            else:
                print("[00:00:00] Setting the input for pin 0.")
                self._input0_pin = value
        elif pin == 1:
            if self._input1_pin is not None:
                raise LogicGateError("Input pin 1 has already been set!")
            else:
                print("[00:00:00] Setting the input for pin 1.")
                self._input1_pin = value
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")
