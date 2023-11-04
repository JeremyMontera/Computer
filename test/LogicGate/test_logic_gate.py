import pytest

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


def test_logic_gate_sanitize_input_error(logic_gate):
    with pytest.raises(AssertionError) as exc:
        logic_gate._sanitize_input(3)

    assert exc.value.args[0] == "3 is not a valid input!"


def test_logic_gate_set_input_pin_error(logic_gate):
    with pytest.raises(NotImplementedError) as exc:
        logic_gate.set_input_pin(0)

    assert exc.value.args[0] == "`set_input_pin` needs to be implemented!"
