from typing import Optional


class LogicGateError(Exception):
    ...


class LogicGate:

    """
    This implements a generic logic gate class. Since the type of logic gate determines
    how many input pins there are, this class will not have any input pins. Every logic
    class does have an output pin and a name.

    Attributes:
        name:           the name of the logic gate class (public)
        output_pin:     the output of the pin that set later on by the logic (private)
    """

    def __init__(self):
        """Constructor..."""

        self._name: str = ""
        """
        The name of the logic gate. This is initially set to a blank string.

        Type:
            string
        """

        self._output_pin: Optional[int] = None
        """
        The output pin of the logic gate. This is initially set to `'None'`.

        TODO: when we implement the `Connection` class, allow this to be either an
        integer or a `Connection` class instance.

        Type:
            integer
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
        This implements how the inputs get transformed into the output. This is
        dependent on what logic gate is running the logic, so for now, this will raise
        a `NotImplementedError` and will need to be implemented by one of the
        descendant classes.

        This is a private method not intended to be directly called by the user.

        Raises:
            NotImplementedError:
                `_logic` needs to be implemented!
        """

        raise NotImplementedError("`_logic` needs to be implemented!")

    def _sanitize_input(self, value: int) -> None:
        """
        This will check the values being set to the input pins. Since inputs are
        assumed to be binary, it checks if the input is 0/1. This is called when
        `set_input_pin` is called by one of the descendants.

        This is a private method not intended to be directly called by the user.

        TODO: update when `Connections` are implemented.
        TODO: make this more flexible to allow for exotic input types?

        Raises:
            {value} is not a valid input!

        Args:
            value:
                The value to be inputted to the logic gate.
        """

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

        Example:
            ```python
            >>> and_gate = AndGate()
            >>> and_gate.set_input_pin(1, pin=0)
            [00:00:00] The input has been validated.
            [00:00:00] Setting the input for pin 0.
            >>> and_gate.set_input_pin(0, pin=1)
            [00:00:00] The input has been validated.
            [00:00:00] Setting the input for pin 1.
            >>> and_gate.get_output_pin()
            [00:00:00] The output pin has not been set yet.
            [00:00:00] Getting the output of the gate.
            0
            ```

        Returns:
            output_pin:
                The value of the output after the logic has been applied to the values
                held by the input pins.
        """

        if self._output_pin is not None:
            print("[00:00:00] The output pin has not been set yet.")

            self._logic()

        print("[00:00:00] Getting the output of the gate.")

        return self._output_pin

    def set_input_pin(self, value: int, pin: int = 0) -> None:
        """
        This will set the input pins. Since the child gate classes could have one or
        more pins, it will allow the user to input the value of an arbitrary pin. As
        such, it will also raise a `NotImplementedError` and will defer implementation
        to child classes.

        The is a public method that can be called by the user, but more than likely, it
        will be called by the `Connection` class, which looks for an input that has
        this method implemented for polymorphism.

        Raises:
            NotImplementedError:
                `set_input_pin` needs to be implemented!

        Args:
            value:
                The value to set the pin to.
            pin:
                (Optional) the pin to set the value to. This defaults to zero to
                handle the case of unary gates.
        """

        raise NotImplementedError("`set_input_pin` needs to be implemented!")
