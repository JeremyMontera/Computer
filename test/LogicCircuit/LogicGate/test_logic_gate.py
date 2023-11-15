import collections
import pytest
from unittest import mock
from typing import List
from Computer.LogicCircuit.LogicGate import LogicGate, LogicType
from Computer.LogicCircuit.LogicGate.logic_gate import LogicGateError


class TestLogicGates:

    gate = collections.namedtuple("gate", ["gtype", "name", "num"])

    not_gate = gate(LogicType.NOT, "foo", 1)
    and_gate = gate(LogicType.AND, "bar", 2)
    or_gate = gate(LogicType.OR, "spam", 2)

    def get_combs(self, num: int) -> List[List[int]]:
        if num == 1:
            return [[1], [0]]
        elif num == 2:
            return [[1, 1], [1, 0], [0, 1], [0, 0]]

    def test_logic_gate_init_error_no_type(self):
        with pytest.raises(LogicGateError) as exc:
            LogicGate(name="blah")

        assert exc.value.args[0] == "You need to pass a valid logic gate type!"

    @pytest.mark.parametrize(
        "config",
        [
            not_gate,
            and_gate,
            or_gate,
        ]
    )
    def test_logic_gate_init(self, config):
        gate = LogicGate(type=config.gtype, name=config.name)

        assert isinstance(gate._type, LogicType)
        assert gate._type == config.gtype
        assert gate._type.value == config.num
        assert isinstance(gate._name, str)
        assert gate._name == config.name
        assert gate._output_pin is None
        assert len(gate._input_pins) == config.num
        assert all(pin is None for pin in gate._input_pins)

    @pytest.mark.parametrize(
        "config",
        [
            not_gate,
            and_gate,
            or_gate,
        ]
    )
    def test_logic_gate_attrs(self, config):
        gate = LogicGate(type=config.gtype, name=config.name)

        assert gate.name == config.name
        gate.name = config.name + "_1"
        assert gate.name == config.name + "_1"
        assert gate.type == config.gtype

    def test_logic_gate__logic_error_input_not_set(self):
        gate = LogicGate(type=LogicType.NOT)
        with pytest.raises(LogicGateError) as exc:
            gate._logic()

        assert exc.value.args[0] == "Pin 0 has not been set yet!"

    @pytest.mark.parametrize(
        "config",
        [
            not_gate,
            and_gate,
            or_gate,
        ]
    )
    def test_logic_gate__logic_pins_are_ints(self, config):
        inputs = self.get_combs(config.num)
        gates = LogicGate(type=config.gtype, name=config.name)
        for i, inp in enumerate(inputs):
            gates._input_pins = inp
            gates._logic()
            assert gates._output_pin is not None
            assert isinstance(gates._output_pin, int)

            if config.gtype == LogicType.NOT:
                logic = not inp[0]
            elif config.gtype == LogicType.AND:
                logic = inp[0] and inp[1]
            elif config.gtype == LogicType.OR:
                logic = inp[0] or inp[1]

            assert gates._output_pin == logic
            gates._input_pins = [None] * config.num
            gates._output_pin = None

    def test_logic_gate__sanitize_input(self):
        gate = LogicGate(type=LogicType.AND)
        with pytest.raises(AssertionError) as exc:
            gate._sanitize_input(2)

        assert exc.value.args[0] == "2 is not a valid input!"

    @mock.patch.object(LogicGate, "_logic")
    def test_logic_gate_get_output_pin(self, mock_logic):
        gate = LogicGate(type=LogicType.AND)
        gate.get_output_pin()
        mock_logic.assert_called_once()
