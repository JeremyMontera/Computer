from Computer.LogicCircuit.Connection import Connection

from .logic_gate import LogicGateError
from .unary_gate import UnaryGate


class NotGate(UnaryGate):

    """
    This implements a not gate. This "is a" type of unary gate. This will implement the
    logic of the Boolean `'and'` operation. It will inherit all of the attributes and
    behaviors of the `UnaryGate` parent class.

    Attributes:
        input0_pin:     the first input pin (private)
        name:           the name of the logic gate class (public)
        output_pin:     the output of the pin that set later on by the logic (private)
    """

    def __init__(self):
        """Constructor..."""

        super().__init__()
        """
        This inherits from the `UnaryGate` parent class.
        """

    def _logic(self) -> None:
        """
        This implements the logic of the Boolean `'not'` operation. It takes the value
        of the one input pin and will set the resulting value to the output pin.

            pin0 | output
            -------------
              0  |   1
              1  |   0

        This is a private method not intended to be directly called by the user.

        Raises:
            LogicGateError:
                The first input pin has not been set!
        """

        if self._input0_pin is None:
            raise LogicGateError("The first input pin has not been set!")

        if isinstance(self._input0_pin, Connection):
            input0 = self._input0_pin.feed()
        elif isinstance(self._input0_pin, int):
            input0 = self._input0_pin

        output = not bool(input0)

        print(f"[00:00:00] not {bool(self._input0_pin)} is {output}.")

        self._output_pin = int(output)
