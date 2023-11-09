import pytest

from Computer.LogicGate import NotGate
from Computer.LogicGate.logic_gate import LogicGateError


@pytest.fixture
def not_gate():
    return NotGate()


def test_and_gate_logic_error(not_gate):
    with pytest.raises(LogicGateError) as exc:
        not_gate._logic()

    assert exc.value.args[0] == "The first input pin has not been set!"


@pytest.mark.parametrize(
    ("pin0", "output"),
    [
        (0, 1),
        (1, 0),
    ],
)
def test_not_gate_logic(pin0, output):
    gate = NotGate()
    gate.set_input_pin(pin0)
    gate._logic()
    assert gate._output_pin == output
