from unittest import mock

import pytest

from Computer.Connection.connection import Connection, ConnectionError
from Computer.LogicGate import LogicGate
from Computer.LogicGate.binary_gate import BinaryGate
from Computer.LogicGate.unary_gate import UnaryGate


@pytest.fixture
def conn():
    return Connection()


def test_connection_feed_error_no_output(conn):
    with pytest.raises(ConnectionError) as exc:
        conn.feed()

    assert exc.value.args[0] == "The output hasn't been connected yet!"


@mock.patch.object(LogicGate, "get_output_pin")
def test_connection_feed(mock_get_output, conn):
    mock_get_output.return_value = 1
    conn._input_connection = LogicGate()
    ret: int = conn.feed()
    mock_get_output.assert_called_once()
    assert ret == 1

def test_connection_set_input_connection_error(conn):
    gate = LogicGate()
    gate.name = "foo"
    gate._output_pin = 0
    with pytest.raises(ConnectionError) as exc:
        conn.set_input_connection(gate)

    assert exc.value.args[0] == "foo's output pin is already set!"

def test_connection_set_input_connection(conn):
    gate = LogicGate()
    gate.name = "bar"
    conn.set_input_connection(gate)
    assert conn._input_connection is not None
    assert conn._input_connection.name == "bar"

def test_connection_set_output_connection_binary_error(conn):
    ...

def test_connection_set_output_connection_binary(conn):
    ...

def test_connection_set_output_connection_unary_error(conn):
    ...

def test_connection_set_output_connection_unary(conn):
    ...
