# from unittest import mock

# import pytest

# from Computer.LogicCircuit import NorGate, NotGate, OrGate
# from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


# @pytest.fixture
# def nor_gate():
#     return NorGate()


# def test_nor_gate_init(nor_gate):
#     assert hasattr(nor_gate, "_input0_pin")
#     assert nor_gate._input0_pin is None
#     assert hasattr(nor_gate, "_input1_pin")
#     assert nor_gate._input1_pin is None
#     assert hasattr(nor_gate, "_output_pin")
#     assert nor_gate._output_pin is None
#     assert hasattr(nor_gate, "_gate0")
#     assert isinstance(nor_gate._gate0, OrGate)
#     assert nor_gate._gate0.name == "nor :: or gate"
#     assert hasattr(nor_gate, "_gate1")
#     assert isinstance(nor_gate._gate1, NotGate)
#     assert nor_gate._gate1.name == "nor :: not gate"
#     assert hasattr(nor_gate, "_conn0")


# @mock.patch.object(NotGate, "get_output_pin")
# def test_nor_gate_get_output_pin(mock_out, nor_gate):
#     nor_gate.get_output_pin()
#     mock_out.assert_called_once


# def test_nor_gate_has_input_pin_set(nor_gate):
#     nor_gate._input0_pin = 0
#     nor_gate._input1_pin = 1
#     assert nor_gate.has_input_pin_set(pin=0)
#     assert nor_gate.has_input_pin_set(pin=1)


# def test_nor_gate_has_input_pin_set_error(nor_gate):
#     with pytest.raises(LogicGateError) as exc:
#         nor_gate.has_input_pin_set(pin=2)

#     assert exc.value.args[0] == "Entered an unknown pin: 2!"


# def test_nor_gate_has_output_pin_set(nor_gate):
#     assert not nor_gate.has_output_pin_set()
#     nor_gate._output_pin = 0
#     assert nor_gate.has_output_pin_set()


# @mock.patch.object(OrGate, "set_input_pin")
# def test_nor_gate_set_input_pin(mock_in, nor_gate):
#     nor_gate.set_input_pin(0, pin=1)
#     mock_in.assert_called_once_with(0, pin=1)
