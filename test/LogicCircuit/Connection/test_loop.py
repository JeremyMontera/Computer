import pytest
from unittest import mock

from Computer.Bit import Bit
from Computer.LogicCircuit.Connection import Loop, LoopError, Connection

def test_loop_init():
    loop = Loop()
    assert hasattr(loop, "_input_connection")
    assert loop._input_connection is None
    assert hasattr(loop, "_output_connections")
    assert len(loop._output_connections) == 2
    assert all(conn is None for conn in loop._output_connections)
    assert hasattr(loop, "_memory")
    assert loop._memory is None

def test_feed_error_bad_index():
    loop = Loop()
    with pytest.raises(LoopError) as exc:
        loop.feed(index=11)

    assert exc.value.args[0] == "You entered an unknown connection: 11!"

def test_feed_error_no_input():
    loop = Loop()
    with pytest.raises(LoopError) as exc:
        loop.feed(index=0)

    assert exc.value.args[0] == "The input connection has not been set yet!"

@mock.patch.object(Connection, "feed")
def test_feed_input_0(mock_feed):
    loop = Loop()
    loop._input_connection = Connection()
    mock_feed.return_value = Bit(0)
    ret: Bit = loop.feed(index=0)
    assert ret == Bit(0)
    assert loop._memory == Bit(0)

def test_feed_error_no_memory():
    loop = Loop()
    with pytest.raises(LoopError) as exc:
        loop.feed(index=1)

    assert exc.value.args[0] == "Looks like no signal came through yet!"

def test_feed_input_1():
    loop = Loop()
    loop._memory = Bit(1)
    ret: Bit = loop.feed(index=1)
    assert ret == Bit(1)

def test_loop_has_input_connection_set():
    loop = Loop()
    assert not loop.has_input_connection_set()
    loop._input_connection = "blah"
    assert loop.has_input_connection_set()

def test_loop_has_output_connection_set_error_bad_conn():
    loop = Loop()
    with pytest.raises(LoopError) as exc:
        loop.has_output_connection_set(index=7)

    assert exc.value.args[0] == "You entered an unknown connection: 7!"

def test_loop_has_output_connection_set():
    loop = Loop()
    assert not loop.has_output_connection_set(index=0)
    assert not loop.has_output_connection_set(index=1)
    loop._output_connections = ("foo", "bar")
    assert loop.has_output_connection_set(index=0)
    assert loop.has_output_connection_set(index=1)

def test_loop_reset():
    loop = Loop()
    loop._input_connection = "blah"
    loop._output_connections = ("red", "yellow")
    loop._memory = 7
    assert loop.has_input_connection_set()
    assert loop.has_output_connection_set(index=0)
    assert loop.has_output_connection_set(index=1)
    assert loop._memory is not None
    loop.reset()
    assert not loop.has_input_connection_set()
    assert not loop.has_output_connection_set(index=0)
    assert not loop.has_output_connection_set(index=1)
    assert loop._memory is None

def test_loop_set_input_connection_error_input_already_set():
    loop = Loop()
    loop._input_connection = 0
    with pytest.raises(LoopError) as exc:
        loop.set_input_connection(conn=Connection())

    assert exc.value.args[0] == "The input connection has already been set!"

def test_loop_set_input_connection():
    loop = Loop()
    loop.set_input_connection(conn=Connection())
    assert loop._input_connection is not None
    assert isinstance(loop._input_connection, Connection)

def test_loop_set_output_connection_error_input_already_set():
    loop = Loop()
    loop._output_connections[1] = 0
    with pytest.raises(LoopError) as exc:
        loop.set_output_connection(conn=Connection(), index=1)

    assert exc.value.args[0] == "Output connection 1 is already connected!"

def test_loop_set_output_connection():
    loop = Loop()
    loop.set_output_connection(conn=Connection(), index=1)
    assert loop._output_connections[0] is None
    assert loop._output_connections[1] is not None
    assert isinstance(loop._output_connections[1], Connection)
