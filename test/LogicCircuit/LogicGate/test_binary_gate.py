import copy

import pytest

from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.LogicGate.binary_gate import BinaryGate
from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


@pytest.fixture
def binary_gate():
    return BinaryGate()


@pytest.fixture
def connection():
    return Connection()


def test_binary_gate_init(binary_gate):
    assert hasattr(binary_gate, "_name")
    assert isinstance(binary_gate._name, str)
    assert binary_gate._name == ""
    assert hasattr(binary_gate, "_type")
    assert isinstance(binary_gate._type, str)
    assert binary_gate.type == "binary"
    assert hasattr(binary_gate, "_output_pin")
    assert binary_gate._output_pin is None
    assert hasattr(binary_gate, "_input0_pin")
    assert hasattr(binary_gate, "_input1_pin")
    assert binary_gate._input0_pin is None
    assert binary_gate._input1_pin is None


def test_binary_gate_logic_error(binary_gate):
    with pytest.raises(NotImplementedError) as exc:
        binary_gate._logic()

    assert exc.value.args[0] == "`_logic` needs to be implemented!"


def test_binary_gate_has_input_pin_set(binary_gate):
    assert not binary_gate.has_input_pin_set(pin=0)
    assert not binary_gate.has_input_pin_set(pin=1)
    binary_gate._input0_pin = 0
    binary_gate._input1_pin = 1
    assert binary_gate.has_input_pin_set(pin=0)
    assert binary_gate.has_input_pin_set(pin=1)


def test_binary_gate_set_input_pin_error_bad_pin(binary_gate):
    with pytest.raises(LogicGateError) as exc:
        binary_gate.set_input_pin(0, pin=3)

    assert exc.value.args[0] == "Entered an unknown pin: 3!"


def test_binary_gate_set_input_pin(binary_gate, connection):
    gate = copy.deepcopy(binary_gate)
    gate.set_input_pin(0)
    assert gate._input0_pin == 0
    gate.set_input_pin(1, pin=1)
    assert gate._input1_pin == 1
    new_gate = copy.deepcopy(binary_gate)
    new_gate.set_input_pin(connection)
    assert isinstance(new_gate._input0_pin, Connection)
    assert new_gate._input0_pin == connection


@pytest.mark.parametrize(
    ("pin",),
    [
        (0,),
        (1,),
    ],
)
def test_binary_gate_set_input_pin_error_pin_set(pin, request):
    binary_gate = BinaryGate()
    binary_gate.set_input_pin(1, pin=pin)
    with pytest.raises(LogicGateError) as exc:
        binary_gate.set_input_pin(0, pin=pin)

    assert exc.value.args[0] == f"Input pin {pin} has already been set!"
