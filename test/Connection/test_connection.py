import pytest
from unittest import mock

from Computer.Connection.connection import Connection, ConnectionError
from Computer.LogicGate import LogicGate

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
    conn._input = LogicGate()
    ret: int = conn.feed()
    mock_get_output.assert_called_once()
    assert ret == 1


