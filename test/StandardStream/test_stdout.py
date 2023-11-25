from unittest import mock

from Computer.StandardStream import StdOut
from Computer.LogicCircuit.Connection import Connection

def test_stdout_init():
    stdout: StdOut = StdOut()
    assert hasattr(stdout, "_input_connections")
    assert isinstance(stdout._input_connections, list)
    assert len(stdout._input_connections) == 0

@mock.patch.object(Connection, "feed")
def test_stdout_print_output(mock_feed):
    stdout: StdOut = StdOut()
    stdout._input_connections = [Connection()]
    stdout.print_output()

    mock_feed.assert_called_once()

def test_stdout_set_input_connection():
    stdout: StdOut = StdOut()
    conn: Connection = Connection()
    stdout.set_input_connection(conn=conn)
    assert len(stdout._input_connections) == 1
    assert stdout._input_connections[0] == conn