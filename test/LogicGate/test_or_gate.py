import pytest

from Computer.LogicGate import OrGate
from Computer.LogicGate.logic_gate import LogicGateError

@pytest.fixture
def or_gate():
    return OrGate()

def test_and_gate_logic_error(or_gate):
    with pytest.raises(LogicGateError) as exc:
        or_gate._logic()

    assert exc.value.args[0] == "The first input pin has not been set!"
    or_gate.set_input_pin(0)
    with pytest.raises(LogicGateError) as exc:
        or_gate._logic()

    assert exc.value.args[0] == "The second input pin has not been set!"

@pytest.mark.parametrize(
    ("pin0", "pin1", "output"),
    [
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ]
)
def test_or_gate_logic(pin0, pin1, output):
    gate = OrGate()
    gate.set_input_pin(pin0, pin=0)
    gate.set_input_pin(pin1, pin=1)
    gate._logic()
    assert gate._output_pin == output
