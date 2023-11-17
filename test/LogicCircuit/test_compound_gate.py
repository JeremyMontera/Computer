import pytest
import collections
from typing import List

from Computer.LogicCircuit import CompoundGate, CompoundType
from Computer.LogicCircuit.compound_gate import CompoundGateError
from Computer.LogicCircuit.LogicGate import LogicGate
from Computer.LogicCircuit.Connection import Connection

class TestCompoundGates:

    cgate = collections.namedtuple("cgate", ["gtype", "name", "fact"])
    nand_gate = cgate(CompoundType.NAND, "foo", "nand")
    nor_gate = cgate(CompoundType.NOR, "bar", "nor")
    xor_gate = cgate(CompoundType.XOR, "eggs", "xor")
    xnor_gate = cgate(CompoundType.XNOR, "spam", "xnor")

    def get_combs(self, num: int) -> List[List[int]]:
        if num == 1:
            return [[1], [0]]
        elif num == 2:
            return [[1, 1], [1, 0], [0, 1], [0, 0]]

    def test_compound_gate_init_error_bad_type(self):
        with pytest.raises(CompoundGateError) as exc:
            CompoundGate()

        assert exc.value.args[0] == "You need to enter a valid logic gate type!"

    @pytest.mark.parametrize(
        ("config", "manifest"),
        [
            (
                nand_gate,
                {
                    "_input_gates": LogicGate,
                    "_output_gate": LogicGate,
                    "_conn0": Connection,
                },
            ),
            (
                nor_gate,
                {
                    "_input_gates": LogicGate,
                    "_output_gate": LogicGate,
                    "_conn0": Connection,
                },
            ),
            (
                xor_gate,
                {
                    "_input_gates": LogicGate,
                    "_gate1": LogicGate,
                    "_output_gate": LogicGate,
                    "_conn0": Connection,
                    "_conn1": Connection,
                    "_conn2": Connection,
                },
            ),
            (
                xnor_gate,
                {
                    "_input_gates": LogicGate,
                    "_gate1": LogicGate,
                    "_gate2": LogicGate,
                    "_output_gate": LogicGate,
                    "_conn0": Connection,
                    "_conn1": Connection,
                    "_conn2": Connection,
                    "_conn3": Connection,
                }
            )
        ]
    )
    def test_compound_gate_init(self, config, manifest):
        gate = CompoundGate(type=config.gtype, name=config.name)
        assert isinstance(gate._type, CompoundType)
        assert gate._type == config.gtype
        assert gate._type.value == config.fact
        assert isinstance(gate._name, str)
        assert gate._name == config.name
        assert hasattr(gate, "_factory")
        assert gate._factory._type == config.fact
        for key, value in manifest.items():
            assert hasattr(gate, key)
            if isinstance(getattr(gate, key), list):
                items = getattr(gate, key)
                assert all(isinstance(item, value) for item in items)
            else:
                assert isinstance(getattr(gate, key), value)

    @pytest.mark.parametrize(
        "config",
        [
            nand_gate,
            nor_gate,
            xor_gate,
            xnor_gate,
        ],
    )
    def test_compound_gate_set_input_pin(self, config):
        gate = CompoundGate(type=config.gtype, name=config.name)
        for g in gate._input_gates:
            assert not g.has_input_pin_set(pin=0)

        gate.set_input_pin(value=1, pin=0)
        for g in gate._input_gates:
            assert g.has_input_pin_set(pin=0)

    @pytest.mark.parametrize(
        "config",
        [
            nand_gate,
            nor_gate,
            xor_gate,
            xnor_gate,
        ],
    )
    def test_compound_gate_set_output_pin(self, config):
        gate = CompoundGate(type=config.gtype, name=config.name)
        conn = Connection()
        assert not gate._output_gate.has_output_pin_set()

        gate.set_output_pin(value=conn)
        assert gate._output_gate.has_output_pin_set()
