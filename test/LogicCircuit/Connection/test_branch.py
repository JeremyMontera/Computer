import pytest
from unittest import mock

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection.connection import Connection
from Computer.LogicCircuit.Connection.branch import Branch, BranchError

@pytest.fixture
def connections():
    opts = ["input", "output"]
    return [(Connection(), opts[(i+1) % 2]) for i in range(5)]

@pytest.fixture
def mapping():
    return {0: 1, 2: 0, 1: 1}

@pytest.fixture
def branch_no_mapping(connections):
    branch = Branch()
    for conn, loc in connections:
        if loc == "input":
            branch._input_connections.append(conn)
        elif loc == "output":
            branch._output_connections.append(conn)

    return branch

@pytest.fixture
def branch_mapping(connections, mapping):
    branch = Branch()
    for conn, loc in connections:
        if loc == "input":
            branch._input_connections.append(conn)
        elif loc == "output":
            branch._output_connections.append(conn)

    branch.set_mapping(mapping=mapping)
    return branch

def test_branch_init():
    branch = Branch()
    assert hasattr(branch, "_input_connections")
    assert isinstance(branch._input_connections, list)
    assert len(branch._input_connections) == 0
    assert hasattr(branch, "_mapping")
    assert branch._mapping is None
    assert hasattr(branch, "_output_connections")
    assert isinstance(branch._output_connections, list)
    assert len(branch._output_connections) == 0

def test_branch_attrs(branch_no_mapping):
    assert branch_no_mapping.num_input_connections == 2
    assert branch_no_mapping.num_output_connections == 3

def test_branch__validate_error_inputs(branch_no_mapping, mapping):
    branch = branch_no_mapping
    branch._input_connections.append(Connection())
    with pytest.raises(AssertionError) as exc:
        branch._validate_mapping(mapping=mapping)

    assert exc.value.args[0] == "Not all of the outputs are connected to inputs!"

def test_branch__validate_error_outputs(branch_no_mapping, mapping):
    branch = branch_no_mapping
    branch._output_connections.append(Connection())
    with pytest.raises(AssertionError) as exc:
        branch._validate_mapping(mapping=mapping)

    assert exc.value.args[0] == "Not all of the outputs have connections!"

def test_branch_feed_error_no_index(branch_mapping):
    with pytest.raises(BranchError) as exc:
        branch_mapping.feed()

    assert exc.value.args[0] == "You need to pass the index to the output connection!"

def test_branch_feed_error_bad_index(branch_mapping):
    with pytest.raises(BranchError) as exc:
        branch_mapping.feed(index=8)

    assert exc.value.args[0] == "8 doesn't correspond to any output connection!"

@mock.patch.object(Connection, "feed")
def test_branch_feed(mock_feed, branch_mapping):
    mock_feed.return_value = Bit(0)
    ret = branch_mapping.feed(index=0)
    assert isinstance(ret, Bit)
    mock_feed.assert_called_once()
    assert ret == Bit(0)

def test_branch_has_set(branch_mapping):
    branch = branch_mapping
    assert branch.has_input_connection_set()
    assert branch.has_output_connection_set()
    assert branch.has_mapping_set()

def test_branch_reset(branch_mapping):
    branch = branch_mapping
    assert len(branch._input_connections) > 0
    assert len(branch._output_connections) > 0
    assert branch._mapping is not None
    branch.reset()
    assert len(branch._input_connections) == 0
    assert len(branch._output_connections) == 0
    assert branch._mapping is None

def test_branch_set_input_connection_error_mapping_set(branch_mapping):
    branch = branch_mapping
    with pytest.raises(BranchError) as exc:
        branch.set_input_connection(Connection())

    assert exc.value.args[0] == (
        "The mapping has been set already! " \
        "You cannot add any more connections!"
    )

def test_branch_set_input_connection_error_no_connection(branch_no_mapping):
    branch = branch_no_mapping
    with pytest.raises(BranchError) as exc:
        branch.set_input_connection()

    assert exc.value.args[0] == "You need to enter a connection!"

def test_branch_set_inpput_connection(connections):
    branch = Branch()
    for conn, loc in connections:
        if loc == "input":
            branch.set_input_connection(conn)

    assert len(branch._input_connections) == 2

def test_branch_set_mapping_error_no_mapping():
    branch = Branch()
    with pytest.raises(BranchError) as exc:
        branch.set_mapping()

    assert exc.value.args[0] == "You need to enter a valid mapping!"

def test_branch_set_mapping_error_mapping_already_set(branch_mapping):
    branch = branch_mapping
    with pytest.raises(BranchError) as exc:
        branch.set_mapping(mapping={3: 4})

    assert exc.value.args[0] == "The mapping has been set already!"

@mock.patch.object(Branch, "_validate_mapping")
def test_branch_set_mapping(mock_validate, branch_no_mapping, mapping):
    branch = branch_no_mapping
    branch.set_mapping(mapping=mapping)
    assert branch._mapping is not None
    assert isinstance(branch._mapping, dict)
    assert branch._mapping == mapping
    mock_validate.assert_called_once_with(mapping)

def test_branch_set_output_connection_error_mapping_set(branch_mapping):
    branch = branch_mapping
    with pytest.raises(BranchError) as exc:
        branch.set_input_connection(Connection())

    assert exc.value.args[0] == (
        "The mapping has been set already! " \
        "You cannot add any more connections!"
    )

def test_branch_set_output_connection_error_no_connection():
    branch = Branch()
    with pytest.raises(BranchError) as exc:
        branch.set_output_connection()

    assert exc.value.args[0] == "You need to enter a connection!"

def test_branch_set_output_connection(connections):
    branch = Branch()
    for conn, loc in connections:
        if loc == "output":
            branch.set_output_connection(conn)

    assert len(branch._output_connections) == 3
