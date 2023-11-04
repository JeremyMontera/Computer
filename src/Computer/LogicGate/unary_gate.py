from typing import Optional

from .logic_gate import LogicGate, LogicGateError


class UnaryGate(LogicGate):
    """
    This implements a unary gate class (i.e., it assumes one input). This "is a" type
    of `LogicGate` and so will inherit attributes/behaviors from said `LogicGate`
    class. However, the logic will be deferred to specific child classes of this class.

    Attributes:
        input0_pin:     the only input pin (private)
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

        self._type: str = "unary"
        """
        The type of logic gate.

        Type:
            string
        """

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        """
        This will set the input pin.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an input that has
        this method implemented for polymorphism.

        Example:
            ```python
            >>> not_gate = NotGate()
            >>> not_gate.set_input_pin(1)
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

        if pin == 0:
            if self._input0_pin is not None:
                raise LogicGateError("Input pin 0 has already been set!")
            else:
                print("[00:00:00] Setting the input for pin 0.")
                self._input0_pin = value
        else:
            raise LogicGateError(f"Entered an unknown pin: {pin}!")
