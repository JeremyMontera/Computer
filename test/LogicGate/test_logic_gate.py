from contextlib import nullcontext as does_not_raise

import pytest

from Computer.Connection import Connection
from Computer.LogicGate.logic_gate import LogicGate


@pytest.fixture
def logic_gate():
    return LogicGate()


def test_logic_gate_init(logic_gate):
    assert hasattr(logic_gate, "_name")
    assert isinstance(logic_gate._name, str)
    assert isinstance(logic_gate._type, str)
    assert logic_gate._name == ""
    assert hasattr(logic_gate, "_output_pin")
    assert logic_gate._output_pin is None


def test_logic_gate_name_attribute(logic_gate):
    logic_gate.name = "Logic Gate"
    assert logic_gate.name == "Logic Gate"


def test_logic_gate_type_attribute(logic_gate):
    assert logic_gate.type == ""


def test_logic_gate_logic_error(logic_gate):
    with pytest.raises(NotImplementedError) as exc:
        logic_gate._logic()

    assert exc.value.args[0] == "`_logic` needs to be implemented!"


@pytest.mark.parametrize(
    ("value", "error", "msg"),
    [
        (3, pytest.raises(AssertionError), "3 is not a valid input!"),
        (Connection(), does_not_raise(), ""),
    ],
)
def test_logic_gate_sanitize_input_error(value, error, msg):
    logic_gate = LogicGate()
    with error as exc:
        logic_gate._sanitize_input(value)

    if isinstance(value, int):
        assert exc.value.args[0] == msg


def test_logic_gate_has_input_set_error(logic_gate):
    with pytest.raises(NotImplementedError) as exc:
        logic_gate.has_input_set(pin=0)

    assert exc.value.args[0] == "`has_input_set` needs to be implemented!"


def test_logic_gate_has_output_set(logic_gate):
    assert not logic_gate.has_output_set()
    logic_gate._output_pin = 0
    assert logic_gate.has_output_set()


def test_logic_gate_set_input_pin_error(logic_gate):
    with pytest.raises(NotImplementedError) as exc:
        logic_gate.set_input_pin(0)

    assert exc.value.args[0] == "`set_input_pin` needs to be implemented!"
