import pytest

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Connection, Branch
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


def test_connection_feed(gate):
    conn = Connection()
    conn._input_connection = gate
    ret: Bit = conn.feed()
    assert ret == Bit(0)


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


def test_connection_set_input_connection_error_device_is_none():
    conn = Connection()
    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection()

    assert exc.value.args[0] == "You need to enter a device to set the input!"


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
    assert conn._input_connection == d
    if device =="gate":
        assert d._output_pin == conn
    elif device == "branch":
        assert d._output_connections == [conn]


def test_connection_set_output_connection_error_device_is_none():
    conn = Connection()
    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection()

    assert exc.value.args[0] == "You need to enter a device to set the output!"


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
    assert conn._output_connection == d
    if device == "gate":
        assert d._input_pins[0] == conn
    elif device == "branch":
        assert d._input_connections == [conn]
