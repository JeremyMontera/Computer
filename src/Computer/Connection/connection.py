from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Computer.LogicGate import LogicGate


class ConnectionError(Exception):
    ...


class Connection:
    def __init__(self):
        self._input_connection: Optional["LogicGate"] = None
        self._output_connection: Optional["LogicGate"] = None

    def feed(self) -> int:
        if self._input_connection is None:
            raise ConnectionError("The output hasn't been connected yet!")

        print(f"[00:00:00] Feeding input gate {self._input_connection.name}'s output.")
        return self._input_connection.get_output_pin()

    def set_input_connection(self, gate: "LogicGate") -> None:
        if gate.has_output_pin_set():
            raise ConnectionError(f"{gate.name}'s output pin is already set!")

        print(f"[00:00:00] Setting {gate.name}'s output pin to the input connection.")
        self._input_connection = gate

    def set_output_connection(self, gate: "LogicGate", pin: int = 0) -> None:
        if pin != 0 and pin != 1:
            raise ConnectionError(f"Entered an unknown pin: {pin}!")
        
        if gate.has_input_pin_set(pin = pin):
            raise ConnectionError(f"{gate.name} already has pin {pin} set!")
        
        print(f"[00:00:00] Setting {gate.name}'s input pin to the output connection.")
        gate.set_input_pin(self, pin=pin)
        self._output_connection = gate
