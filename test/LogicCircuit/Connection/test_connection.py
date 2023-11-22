from unittest import mock

import pytest

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Branch, Connection, Loop, Switch
from Computer.LogicCircuit.Connection.connection import ConnectionError
from Computer.LogicCircuit.LogicGate import LogicGate, LogicType


@pytest.fixture
def gate():
    return LogicGate(type=LogicType.AND, name="foo")


@pytest.fixture
def branch():
    return Branch()


@pytest.fixture
def switch():
    return Switch()


@pytest.fixture
def loop():
    return Loop()


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


@mock.patch.object(LogicGate, "get_output_pin")
def test_connection_feed_gate(mock_get, gate):
    mock_get.return_value = Bit(0)
    conn = Connection()
    conn._input_connection = gate
    ret: Bit = conn.feed()
    assert ret == Bit(0)
    mock_get.assert_called_once()


@mock.patch.object(Branch, "feed")
def test_connection_feed_branch(mock_feed, branch):
    mock_feed.return_value = Bit(1)
    conn = Connection()
    conn._input_connection = (branch, 2)
    ret: Bit = conn.feed()
    assert ret == Bit(1)
    mock_feed.assert_called_once_with(index=2)


@mock.patch.object(Switch, "feed")
def test_connection_feed_switch(mock_feed, switch):
    mock_feed.return_value = Bit(1)
    conn = Connection()
    conn._input_connection = switch
    ret: Bit = conn.feed()
    assert ret == Bit(1)
    mock_feed.assert_called_once()


@mock.patch.object(Loop, "feed")
def test_connection_feed_loop(mock_feed, loop):
    mock_feed.return_value = Bit(0)
    conn = Connection()
    conn._input_connection = (loop, 1)
    ret: Bit = conn.feed()
    assert ret == Bit(0)
    mock_feed.assert_called_once_with(index=1)


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
        "switch",
        "loop",
    ],
)
def test_connection_set_input_connection_error_device_connected(device, request):
    d = request.getfixturevalue(device)
    conn = Connection()
    if device == "gate":
        d._output_pin = 0
    elif device == "switch":
        d._output_connection = "blue"
    elif device == "loop":
        d._output_connections[0] = "ten"

    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection(device=d, index=0)

    if device == "gate":
        assert exc.value.args[0] == "foo's output is already connected!"
    elif device == "switch":
        assert exc.value.args[0] == "This switch is already fully connected!"
    elif device == "loop":
        assert exc.value.args[0] == (
            "Output connection 0 of this loop is already connected!"
        )


@pytest.mark.parametrize(
    "device",
    [
        "gate",
        "branch",
        "switch",
        "loop",
    ],
)
def test_connection_set_input_connection(device, request):
    conn = Connection()
    d = request.getfixturevalue(device)
    conn.set_input_connection(device=d, index=1)
    if device == "gate":
        assert conn._input_connection == d
        assert d._output_pin == conn
    elif device == "branch":
        assert conn._input_connection == (d, 0)
        assert d._output_connections == [conn]
    elif device == "switch":
        assert conn._input_connection == d
        assert d._output_connection == conn
    elif device == "loop":
        assert conn._input_connection == (d, 1)
        assert d._output_connections[1] == conn


def test_connection_set_output_connection_error_conn_already_connected(gate):
    conn = Connection()
    conn._output_connection = gate
    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection(device=gate, index=0)

    assert exc.value.args[0] == "An output connection has already been made!"


@pytest.mark.parametrize(
    "device",
    [
        "gate",
        "switch",
        "loop",
    ],
)
def test_connection_set_output_connection_error_device_connected(device, request):
    d = request.getfixturevalue(device)
    conn = Connection()
    if device == "gate":
        d._input_pins[0] = 0
    elif device == "switch":
        d._input_connections[0] = "red"
    elif device == "loop":
        d._input_connection = "blah"

    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection(device=d, index=0)

    if device == "gate":
        assert exc.value.args[0] == "foo's input is already connected!"
    elif device == "switch":
        assert exc.value.args[0] == "This switch is already fully connected!"
    elif device == "loop":
        assert exc.value.args[0] == "This loop is already connected!"


@pytest.mark.parametrize(
    "device",
    [
        "gate",
        "branch",
        "switch",
        "loop",
    ],
)
def test_connection_set_output_connection(device, request):
    conn = Connection()
    d = request.getfixturevalue(device)
    d.reset()
    conn.set_output_connection(device=d, index=0)
    if device == "gate":
        assert conn._output_connection == d
        assert d._input_pins[0] == conn
    elif device == "branch":
        assert conn._output_connection == (d, 1)
        assert d._input_connections == [conn]
    elif device == "switch":
        assert conn._output_connection == d
        assert d._input_connections[0] == conn
    elif device == "loop":
        assert conn._output_connection == d
        assert d._input_connection == conn
