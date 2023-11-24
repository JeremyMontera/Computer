from Computer.Bit import Bit, BitString
from Computer.LogicCircuit.Connection import Connection
from Computer.StandardStream import StdIn

def test_stdin_init():
    stdin = StdIn()
    assert hasattr(stdin, "_input_connections")
    assert isinstance(stdin._input_connections, list)
    assert len(stdin._input_connections) == 0
    assert hasattr(stdin, "_value")
    assert isinstance(stdin._value, BitString)
    assert len(stdin._value) == 0

def test_stdin_attrs():
    stdin = StdIn()
    stdin._value.push_right(Bit(0))
    stdin._value.push_right(Bit(1))
    assert len(stdin.value) == 2
    assert stdin.value._bits == [Bit(0), Bit(1)]