from unittest import mock

import pytest

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Branch, Connection
from Computer.LogicCircuit.Connection.connection import ConnectionError
from Computer.LogicCircuit.LogicGate import LogicGate, LogicType


@pytest.fixture
def gate():
    gate = LogicGate(LogicType.AND)
    gate.name = "foo"
    gate.set_input_pin(value=Bit(0), pin=0)
    gate.set_input_pin(value=Bit(1), pin=1)
    return gate


@pytest.fixture
def branch():
    return Branch()


def test_connection_init():
    conn = Connection()
    assert hasattr(conn, "_input_connection")
    assert conn._input_connection is None
    assert hasattr(conn, "_output_connection")
    assert conn._output_connection is None


def test_connection_feed_error_no_ouput():
    conn = Connection()
    with pytest.raises(ConnectionError) as exc:
        conn.feed()

    assert exc.value.args[0] == "The output connection has not been set yet!"


def test_connection_feed_gate(gate):
    conn = Connection()
    conn._input_connection = gate
    ret: Bit = conn.feed()
    assert ret == Bit(0)


@mock.patch.object(LogicGate, "get_output_pin")
def test_connection_feed_branch(mock_get, branch, gate):
    conn0 = Connection()
    conn1 = Connection()
    conn0._input_connection = (branch, 1)
    conn1._input_connection = gate
    conn1._output_connection = (branch, 1)
    branch._output_connections = [conn0]
    branch._input_connections = [conn1]
    branch._mapping = {0: 0}
    mock_get.return_value = Bit(1)
    ret = conn0.feed()

    assert isinstance(ret, Bit)
    assert ret == Bit(1)


def test_has_input_connection_set(gate):
    conn = Connection()
    assert not conn.has_input_connection_set()
    conn._input_connection = gate
    assert conn.has_input_connection_set()


def test_has_output_connection_set(gate):
    conn = Connection()
    assert not conn.has_output_connection_set()
    conn._output_connection = gate
    assert conn.has_output_connection_set()


def test_connection_reset(gate):
    conn = Connection()
    conn._input_connection = gate
    conn._output_connection = gate
    assert conn.has_input_connection_set()
    assert conn.has_output_connection_set()
    conn.reset()
    assert not conn.has_input_connection_set()
    assert not conn.has_output_connection_set()


def test_connection_set_input_connection_error_conn_already_connected(gate):
    conn = Connection()
    conn._input_connection = gate
    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection(device=gate)

    assert exc.value.args[0] == "An input connection has already been made!"


@pytest.mark.parametrize(
    "device",
    [
        "gate",
        "branch",
    ],
)
def test_connection_set_input_connection(device, request):
    conn = Connection()
    d = request.getfixturevalue(device)
    conn.set_input_connection(device=d)
    if device == "gate":
        assert conn._input_connection == d
        assert d._output_pin == conn
    elif device == "branch":
        assert conn._input_connection == (d, 1)
        assert d._output_connections == [conn]


def test_connection_set_output_connection_error_conn_already_connected(gate):
    conn = Connection()
    conn._output_connection = gate
    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection(device=gate, pin=0)

    assert exc.value.args[0] == "An output connection has already been made!"


@pytest.mark.parametrize(
    "device",
    [
        "gate",
        "branch",
    ],
)
def test_connection_set_output_connection(device, request):
    conn = Connection()
    d = request.getfixturevalue(device)
    d.reset()
    conn.set_output_connection(device=d, pin=0)
    if device == "gate":
        assert conn._output_connection == d
        assert d._input_pins[0] == conn
    elif device == "branch":
        assert conn._output_connection == (d, 1)
        assert d._input_connections == [conn]
