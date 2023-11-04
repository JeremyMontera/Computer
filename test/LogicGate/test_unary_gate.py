import copy

import pytest

from Computer.Connection import Connection
from Computer.LogicGate.logic_gate import LogicGateError
from Computer.LogicGate.unary_gate import UnaryGate


@pytest.fixture
def unary_gate():
    return UnaryGate()


@pytest.fixture
def connection():
    return Connection()


def test_unary_gate_init(unary_gate):
    assert hasattr(unary_gate, "_name")
    assert isinstance(unary_gate._name, str)
    assert unary_gate._name == ""
    assert hasattr(unary_gate, "_type")
    assert isinstance(unary_gate._type, str)
    assert unary_gate.type == "unary"
    assert hasattr(unary_gate, "_output_pin")
    assert unary_gate._output_pin is None
    assert hasattr(unary_gate, "_input0_pin")
    assert unary_gate._input0_pin is None


def test_unary_gate_logic_error(unary_gate):
    with pytest.raises(NotImplementedError) as exc:
        unary_gate._logic()

    assert exc.value.args[0] == "`_logic` needs to be implemented!"


def test_unary_gate_has_input_set(unary_gate):
    assert not unary_gate.has_input_set(pin=0)
    unary_gate._input0_pin = 0
    assert unary_gate.has_input_set(pin=0)


def test_unary_gate_set_input_pin_error_bad_pin(unary_gate):
    with pytest.raises(LogicGateError) as exc:
        unary_gate.set_input_pin(0, pin=3)

    assert exc.value.args[0] == "Entered an unknown pin: 3!"


def test_unary_gate_set_input_pin(unary_gate, connection):
    gate = copy.deepcopy(unary_gate)
    gate.set_input_pin(0)
    assert gate._input0_pin == 0
    new_gate = copy.deepcopy(unary_gate)
    new_gate.set_input_pin(connection)
    assert isinstance(new_gate._input0_pin, Connection)
    assert new_gate._input0_pin == connection


def test_unary_gate_set_input_pin_error_pin_set(unary_gate):
    unary_gate.set_input_pin(1)
    with pytest.raises(LogicGateError) as exc:
        unary_gate.set_input_pin(0)

    assert exc.value.args[0] == "Input pin 0 has already been set!"
