import pytest

from Computer.LogicCircuit import CompoundError, CompoundFactory


@pytest.fixture
def nand_manifest():
    return {
        "gate0": "and_0",
        "gate1": "not_0",
        "conn0": ["and_0", "not_0", 0],
    }


@pytest.fixture
def nor_manifest():
    return {
        "gate0": "or_0",
        "gate1": "not_0",
        "conn0": ["or_0", "not_0", 0],
    }


@pytest.fixture
def xor_manifest():
    return {
        "gate0": "and_0",
        "gate1": "not_0",
        "gate2": "and_1",
        "gate3": "and_2",
        "conn0": ["and_0", "not_0", 0],
        "conn1": ["not_0", "and_2", 0],
        "conn2": ["and_1", "and_2", 1],
    }


@pytest.fixture
def xnor_manifest():
    return {
        "gate0": "and_0",
        "gate1": "not_0",
        "gate2": "and_1",
        "gate3": "and_2",
        "gate4": "not_1",
        "conn0": ["and_0", "not_0", 0],
        "conn1": ["not_0", "and_2", 0],
        "conn2": ["and_1", "and_2", 1],
        "conn3": ["and_2", "not_1", 0],
    }


def test_factory_init_error_bad_type():
    with pytest.raises(CompoundError) as exc:
        CompoundFactory()

    assert exc.value.args[0] == "You need to pass a valid compound logic gate type!"


def test_factory_init():
    fact = CompoundFactory("xor")
    assert hasattr(fact, "_type")
    assert isinstance(fact._type, str)
    assert fact._type == "xor"


@pytest.mark.parametrize(
    ("config", "results"),
    [
        ("nand", "nand_manifest"),
        ("nor", "nor_manifest"),
        ("xor", "xor_manifest"),
        ("xnor", "xnor_manifest"),
    ],
)
def test_factory_create(config, results, request):
    manifest = request.getfixturevalue(results)
    fact = CompoundFactory(config)
    res = fact.create()

    assert len(res) == len(manifest)
    for key in manifest.keys():
        assert key in res.keys()
        if "gate" in key:
            assert manifest[key] == res[key].name
        elif "conn" in key:
            assert res[key].has_input_connection_set()
            assert res[key].has_output_connection_set()
            assert res[key]._input_connection.name == manifest[key][0]
            assert res[key]._output_connection.name == manifest[key][1]
            assert res[key]._output_connection.has_input_pin_set(pin=manifest[key][2])
