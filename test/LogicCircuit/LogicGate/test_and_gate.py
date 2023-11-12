import pytest

from Computer.LogicCircuit.LogicGate import AndGate
from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


@pytest.fixture
def and_gate():
    return AndGate()


def test_and_gate_logic_error(and_gate):
    with pytest.raises(LogicGateError) as exc:
        and_gate._logic()

    assert exc.value.args[0] == "The first input pin has not been set!"
    and_gate.set_input_pin(0)
    with pytest.raises(LogicGateError) as exc:
        and_gate._logic()

    assert exc.value.args[0] == "The second input pin has not been set!"


@pytest.mark.parametrize(
    ("pin0", "pin1", "output"),
    [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 1),
    ],
)
def test_and_gate_logic(pin0, pin1, output):
    gate = AndGate()
    gate.set_input_pin(pin0, pin=0)
    gate.set_input_pin(pin1, pin=1)
    gate._logic()
    assert gate._output_pin == output
