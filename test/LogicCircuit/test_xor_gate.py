from unittest import mock

import pytest

from Computer.LogicCircuit import AndGate, NandGate, XorGate
from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


@pytest.fixture
def xor_gate():
    return XorGate()


def test_xor_gate_init(xor_gate):
    assert hasattr(xor_gate, "_input0_pin")
    assert xor_gate._input0_pin is None
    assert hasattr(xor_gate, "_input1_pin")
    assert xor_gate._input1_pin is None
    assert hasattr(xor_gate, "_output_pin")
    assert xor_gate._output_pin is None
    assert hasattr(xor_gate, "_gate0")
    assert isinstance(xor_gate._gate0, NandGate)
    assert xor_gate._gate0.name == "xor :: nand gate"
    assert hasattr(xor_gate, "_gate1")
    assert isinstance(xor_gate._gate1, AndGate)
    assert xor_gate._gate1.name == "xor :: and gate 0"
    assert hasattr(xor_gate, "_gate2")
    assert isinstance(xor_gate._gate2, AndGate)
    assert xor_gate._gate2.name == "xor :: and gate 1"
    assert hasattr(xor_gate, "_conn0")
    assert hasattr(xor_gate, "_conn1")


@mock.patch.object(AndGate, "get_output_pin")
def test_xnor_gate_get_output_pin(mock_out, xor_gate):
    xor_gate.get_output_pin()
    mock_out.assert_called_once


def test_xnor_gate_has_input_pin_set(xor_gate):
    xor_gate._input0_pin = 0
    xor_gate._input1_pin = 1
    assert xor_gate.has_input_pin_set(pin=0)
    assert xor_gate.has_input_pin_set(pin=1)


def test_xnor_gate_has_input_pin_set_error(xor_gate):
    with pytest.raises(LogicGateError) as exc:
        xor_gate.has_input_pin_set(pin=2)

    assert exc.value.args[0] == "Entered an unknown pin: 2!"


def test_xnor_gate_has_output_pin_set(xor_gate):
    assert not xor_gate.has_output_pin_set()
    xor_gate._output_pin = 0
    assert xor_gate.has_output_pin_set()


@mock.patch.object(NandGate, "set_input_pin")
@mock.patch.object(AndGate, "set_input_pin")
def test_xnor_gate_set_input_pin(mock_and_in, mock_nand_in, xor_gate):
    xor_gate.set_input_pin(0, pin=1)
    mock_nand_in.assert_called_once_with(0, pin=1)
    mock_and_in.assert_called_once_with(0, pin=1)
