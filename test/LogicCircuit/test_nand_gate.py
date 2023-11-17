# from unittest import mock

# import pytest

# from Computer.LogicCircuit import AndGate, NandGate, NotGate
# from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


# @pytest.fixture
# def nand_gate():
#     return NandGate()


# def test_nand_gate_init(nand_gate):
#     assert hasattr(nand_gate, "_input0_pin")
#     assert nand_gate._input0_pin is None
#     assert hasattr(nand_gate, "_input1_pin")
#     assert nand_gate._input1_pin is None
#     assert hasattr(nand_gate, "_output_pin")
#     assert nand_gate._output_pin is None
#     assert hasattr(nand_gate, "_gate0")
#     assert isinstance(nand_gate._gate0, AndGate)
#     assert nand_gate._gate0.name == "nand :: and gate"
#     assert hasattr(nand_gate, "_gate1")
#     assert isinstance(nand_gate._gate1, NotGate)
#     assert nand_gate._gate1.name == "nand :: not gate"
#     assert hasattr(nand_gate, "_conn0")


# @mock.patch.object(NotGate, "get_output_pin")
# def test_nand_gate_get_output_pin(mock_out, nand_gate):
#     nand_gate.get_output_pin()
#     mock_out.assert_called_once


# def test_nand_gate_has_input_pin_set(nand_gate):
#     nand_gate._input0_pin = 0
#     nand_gate._input1_pin = 1
#     assert nand_gate.has_input_pin_set(pin=0)
#     assert nand_gate.has_input_pin_set(pin=1)


# def test_nand_gate_has_input_pin_set_error(nand_gate):
#     with pytest.raises(LogicGateError) as exc:
#         nand_gate.has_input_pin_set(pin=2)

#     assert exc.value.args[0] == "Entered an unknown pin: 2!"


# def test_nand_gate_has_output_pin_set(nand_gate):
#     assert not nand_gate.has_output_pin_set()
#     nand_gate._output_pin = 0
#     assert nand_gate.has_output_pin_set()


# @mock.patch.object(AndGate, "set_input_pin")
# def test_nand_gate_set_input_pin(mock_in, nand_gate):
#     nand_gate.set_input_pin(0, pin=1)
#     mock_in.assert_called_once_with(0, pin=1)
