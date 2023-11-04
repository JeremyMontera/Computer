from .binary_gate import BinaryGate
from .logic_gate import LogicGateError


class AndGate(BinaryGate):

    """
    This implements an and gate. This "is a" type of binary gate. This will implement
    the logic of the Boolean `'and'` operation. It will inherit all of the attributes
    and behaviors of the `BinaryGate` parent class.

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
        This inherits from the `BinaryGate` parent class.
        """

    def _logic(self) -> None:
        """
        This implements the logic of the Boolean `'and'` operation. It takes the value
        of the two input pins and will set the resulting value to the output pin.

            pin0 | pin1 | output
            --------------------
              0  |  0   |    0
              0  |  1   |    0
              1  |  0   |    0
              1  |  1   |    1

        This is a private method not intended to be directly called by the user.

        Raises:
            LogicGateError:
                (1) The first input pin has not been set!
                (2) The second input pin has not been set!
        """

        if self._input0_pin is None:
            raise LogicGateError("The first input pin has not been set!")
        elif self._input1_pin is None:
            raise LogicGateError("The second input pin has not been set!")

        output = bool(self._input0_pin) and bool(self._input1_pin)

        print(
            f"[00:00:00] {bool(self._input0_pin)} and {bool(self._input1_pin)} is "
            f"{output}."
        )

        self._output_pin = int(output)
