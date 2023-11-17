import collections
from typing import List
from unittest import mock

import pytest

from Computer.LogicCircuit.Connection import Connection
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
        ],
    )
    def test_logic_gate_init(self, config):
        gate = LogicGate(type=config.gtype, name=config.name)

        assert isinstance(gate._type, LogicType)
        assert gate._type == config.gtype
        assert isinstance(gate._name, str)
        assert gate._name == config.name
        assert len(gate._input_pins) == config.num
        assert all(pin is None for pin in gate._input_pins)
        assert gate._output_pin is None

    @pytest.mark.parametrize(
        "config",
        [
            not_gate,
            and_gate,
            or_gate,
        ],
    )
    def test_logic_gate_attrs(self, config):
        gate = LogicGate(type=config.gtype, name=config.name)

        assert gate.name == config.name
        gate.name = config.name + "_1"
        assert gate.name == config.name + "_1"
        assert gate.type == config.gtype

    def test_logic_gate__sanitize_input(self):
        gate = LogicGate(type=LogicType.AND)
        with pytest.raises(AssertionError) as exc:
            gate._sanitize_input(2)

        assert exc.value.args[0] == "2 is not a valid input!"

    def test_logic_gate_get_output_pin_input_not_set(self):
        gate = LogicGate(type=LogicType.NOT)
        with pytest.raises(LogicGateError) as exc:
            gate.get_output_pin()

        assert exc.value.args[0] == "Pin 0 has not been set yet!"

    @pytest.mark.parametrize(
        "config",
        [
            not_gate,
            and_gate,
            or_gate,
        ],
    )
    def test_logic_gate_get_output_pin_ints(self, config):
        inputs = self.get_combs(config.num)
        gates = LogicGate(type=config.gtype, name=config.name)
        for inp in inputs:
            gates._input_pins = inp
            ret = gates.get_output_pin()
            assert isinstance(ret, int)

            if config.gtype == LogicType.NOT:
                logic = not inp[0]
            elif config.gtype == LogicType.AND:
                logic = inp[0] and inp[1]
            elif config.gtype == LogicType.OR:
                logic = inp[0] or inp[1]

            assert ret == logic
            gates._input_pins = [None] * config.num
            gates._output_pin = None

    def test_logic_gate_has_input_pin_set_error_bad_pin(self):
        gate = LogicGate(LogicType.AND)
        with pytest.raises(LogicGateError) as exc:
            gate.has_input_pin_set(pin=2)

        assert exc.value.args[0] == "Entered an invalid pin: 2!"

    def test_logic_gate_has_input_pin_set(self):
        gate = LogicGate(LogicType.AND)
        for p in range(2):
            assert not gate.has_input_pin_set(pin=p)
            gate._input_pins[p] = 0
            assert gate.has_input_pin_set(pin=p)

    def test_logic_gate_has_output_pin_set(self):
        gate = LogicGate(LogicType.AND)
        assert not gate.has_output_pin_set()
        gate._output_pin = 1
        assert gate.has_output_pin_set()

    def test_logic_gate_reset(self):
        gate = LogicGate(LogicType.AND)
        gate._input_pins = [0, 1]
        gate._output_pin = 1
        assert gate.has_input_pin_set(pin=0)
        assert gate.has_input_pin_set(pin=1)
        assert gate.has_output_pin_set()
        gate.reset()
        assert not gate.has_input_pin_set(pin=0)
        assert not gate.has_input_pin_set(pin=1)
        assert not gate.has_output_pin_set()

    def test_logic_gate_set_input_pin_error_pin_already_set(self):
        gate = LogicGate(LogicType.AND)
        gate._input_pins[0] = 1
        with pytest.raises(LogicGateError) as exc:
            gate.set_input_pin(value=0, pin=0)

        assert exc.value.args[0] == "Input pin 0 has already been set!"

    @mock.patch.object(LogicGate, "_sanitize_input")
    def test_logic_gate_set_input_pin(self, mock_sanitize):
        gate = LogicGate(LogicType.AND)
        gate.set_input_pin(value=1, pin=0)
        assert gate._input_pins[0] == 1
        mock_sanitize.assert_called_once_with(0)

    def test_logic_gate_set_output_pin_error_value_none(self):
        gate = LogicGate(LogicType.AND)
        with pytest.raises(LogicGateError) as exc:
            gate.set_output_pin()

        assert exc.value.args[0] == "You need to enter a valid connection!"

    def test_logic_gate_set_output_pin_error_pin_already_set(self):
        gate = LogicGate(LogicType.AND)
        conn = Connection()
        gate._output_pin = conn
        with pytest.raises(LogicGateError) as exc:
            gate.set_output_pin(value=conn)

        assert exc.value.args[0] == "The output pin has already been set!"

    def test_logic_gate_set_output_pin(self):
        gate = LogicGate(LogicType.AND)
        assert not gate.has_output_pin_set()
        conn = Connection()
        gate.set_output_pin(value=conn)
        assert gate.has_output_pin_set()
