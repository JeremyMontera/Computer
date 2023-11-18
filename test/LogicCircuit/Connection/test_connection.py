import pytest

from Computer.LogicCircuit.Connection import Connection
from Computer.LogicCircuit.Connection.connection import ConnectionError
from Computer.LogicCircuit.LogicGate import LogicGate, LogicType


@pytest.fixture
def gate():
    gate = LogicGate(LogicType.AND)
    gate.name = "foo"
    gate.set_input_pin(value=0, pin=0)
    gate.set_input_pin(value=1, pin=1)
    return gate


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
    ret: int = conn.feed()
    assert ret == 0


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


def test_connection_set_input_connection_error_gate_is_none():
    conn = Connection()
    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection()

    assert exc.value.args[0] == "You need to enter a gate to set the input!"


def test_connection_set_input_connection_error_conn_already_connected(gate):
    conn = Connection()
    conn._input_connection = gate
    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection(gate=gate)

    assert exc.value.args[0] == "An input connection has already been made!"


def test_connection_set_input_connection(gate):
    conn = Connection()
    conn.set_input_connection(gate=gate)
    assert conn._input_connection == gate
    assert gate._output_pin == conn


def test_connection_set_output_connection_error_gate_is_none():
    conn = Connection()
    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection()

    assert exc.value.args[0] == "You need to enter a gate to set the output!"


def test_connection_set_output_connection_error_conn_already_connected(gate):
    conn = Connection()
    conn._output_connection = gate
    with pytest.raises(ConnectionError) as exc:
        conn.set_output_connection(gate=gate, pin=0)

    assert exc.value.args[0] == "An output connection has already been made!"


def test_connection_set_output_connection(gate):
    conn = Connection()
    gate.reset()
    conn.set_output_connection(gate=gate, pin=0)
    assert conn._output_connection == gate
    assert gate._input_pins[0] == conn
