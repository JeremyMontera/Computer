from unittest import mock

from Computer.Bit import Bit, BitString
from Computer.LogicCircuit.Connection import Connection
from Computer.StandardStream import StdIn

def test_stdin_init():
    stdin = StdIn(max_length=10)
    assert hasattr(stdin, "_input_connections")
    assert isinstance(stdin._input_connections, list)
    assert len(stdin._input_connections) == 0
    assert hasattr(stdin, "_stored_values")
    assert isinstance(stdin._stored_values, BitString)
    assert len(stdin._stored_values) == 0
    assert stdin._stored_values.max_length == 10

def test_stdin_attrs():
    stdin = StdIn(max_length=10)
    stdin._stored_values.push_right(Bit(0))
    stdin._stored_values.push_right(Bit(1))
    assert len(stdin.stored_values) == 2
    assert stdin.stored_values._bits == [Bit(0), Bit(1)]

def test_stdin_feed():
    stdin = StdIn(max_length=10)
    stdin._stored_values.push_right(Bit(0))
    assert len(stdin._stored_values) == 1
    assert stdin.feed() == Bit(0)
    assert len(stdin._stored_values) == 0

def test_stdin_set_input_connection():
    stdin = StdIn(max_length=10)
    conn = Connection()
    stdin.set_input_connection(conn=conn)
    assert len(stdin._input_connections) == 1

def test_stdin_set_input_value():
    stdin = StdIn(max_length=10)
    stuff = BitString(max_length=3)
    stuff._bits = [Bit(0), Bit(1)]
    stdin.set_input_value(value=stuff)
    assert len(stdin._stored_values) == 2
    stdin.set_input_value(value=Bit(1))
    assert len(stdin._stored_values) == 3
