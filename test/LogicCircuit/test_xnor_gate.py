import pytest
from unittest import mock

from Computer.LogicCircuit import XorGate, XnorGate, NotGate
from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError

@pytest.fixture
def xnor_gate():
    return XnorGate()

def test_xnor_gate_init(xnor_gate):
    assert hasattr(xnor_gate, "_input0_pin")
    assert xnor_gate._input0_pin is None
    assert hasattr(xnor_gate, "_input1_pin")
    assert xnor_gate._input1_pin is None
    assert hasattr(xnor_gate, "_output_pin")
    assert xnor_gate._output_pin is None
    assert hasattr(xnor_gate, "_gate0")
    assert isinstance(xnor_gate._gate0, XorGate)
    assert xnor_gate._gate0.name == "xnor :: xor gate"
    assert hasattr(xnor_gate, "_gate1")
    assert isinstance(xnor_gate._gate1, NotGate)
    assert xnor_gate._gate1.name == "xnor :: not gate"
    assert hasattr(xnor_gate, "_conn0")

@mock.patch.object(NotGate, "get_output_pin")
def test_xnor_gate_get_output_pin(mock_out, xnor_gate):
    xnor_gate.get_output_pin()
    mock_out.assert_called_once

def test_xnor_gate_has_input_pin_set(xnor_gate):
    xnor_gate._input0_pin = 0
    xnor_gate._input1_pin = 1
    assert xnor_gate.has_input_pin_set(pin=0)
    assert xnor_gate.has_input_pin_set(pin=1)

def test_xnor_gate_has_input_pin_set_error(xnor_gate):
    with pytest.raises(LogicGateError) as exc:
        xnor_gate.has_input_pin_set(pin=2)

    assert exc.value.args[0] == "Entered an unknown pin: 2!"

def test_xnor_gate_has_output_pin_set(xnor_gate):
    assert not xnor_gate.has_output_pin_set()
    xnor_gate._output_pin = 0
    assert xnor_gate.has_output_pin_set()

@mock.patch.object(XorGate, "set_input_pin")
def test_xnor_gate_set_input_pin(mock_in, xnor_gate):
    xnor_gate.set_input_pin(0, pin=1)
    mock_in.assert_called_once_with(0, pin=1)
