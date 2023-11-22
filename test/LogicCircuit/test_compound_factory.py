import pytest

from Computer.LogicCircuit import CompoundFactory


@pytest.fixture
def nand_manifest():
    return {
        "input_gates": ["and_0"],
        "output_gate": "not_0",
        "conn0": ["and_0", "not_0", 0],
    }


@pytest.fixture
def nor_manifest():
    return {
        "input_gates": ["or_0"],
        "output_gate": "not_0",
        "conn0": ["or_0", "not_0", 0],
    }


@pytest.fixture
def xor_manifest():
    return {
        "input_gates": ["and_0", "or_0"],
        "gate1": "not_0",
        "output_gate": "and_1",
        "conn0": ["and_0", "not_0", 0],
        "conn1": ["not_0", "and_1", 0],
        "conn2": ["or_0", "and_1", 1],
    }


@pytest.fixture
def xnor_manifest():
    return {
        "input_gates": ["and_0", "or_0"],
        "gate1": "not_0",
        "gate2": "and_1",
        "output_gate": "not_1",
        "conn0": ["and_0", "not_0", 0],
        "conn1": ["not_0", "and_1", 0],
        "conn2": ["or_0", "and_1", 1],
        "conn3": ["and_1", "not_1", 0],
    }


def test_factory_init():
    fact = CompoundFactory(type="xor")
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
    fact = CompoundFactory(type=config)
    res = fact.create()

    assert len(res) == len(manifest)
    for key in manifest.keys():
        assert key in res.keys()
        if "gate" in key:
            if isinstance(manifest[key], list):
                assert len(manifest[key]) == len(res[key])
                assert all(
                    res[key][i].name == manifest[key][i]
                    for i in range(len(manifest[key]))
                )
            else:
                assert manifest[key] == res[key].name
        elif "conn" in key:
            assert res[key].has_input_connection_set()
            assert res[key].has_output_connection_set()
            assert res[key]._input_connection.name == manifest[key][0]
            assert res[key]._output_connection.name == manifest[key][1]
            assert res[key]._output_connection.has_input_pin_set(pin=manifest[key][2])
