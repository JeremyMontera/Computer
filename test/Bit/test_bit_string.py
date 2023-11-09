import pytest

from Computer.Bit import Bit, BitString


@pytest.fixture
def bits():
    bits: BitString = BitString(5)
    bits.push_right(Bit(0))
    bits.push_right(Bit(1))
    bits.push_right(Bit(0))
    return bits


def test_bit_string_init():
    empty: BitString = BitString(10)
    assert isinstance(empty._max_length, int)
    assert empty._max_length == 10
    assert isinstance(empty._bits, list)
    assert empty._bits == []


def test_bit_string_max_length(bits):
    assert bits.max_length == 5


def test_bit_string_iter(bits):
    res = [0, 1, 0]
    for bit0, bit1 in zip(bits, res):
        assert isinstance(bit0, Bit)
        assert int(bool(bit0)) == bit1


def test_bit_string_length(bits):
    assert len(bits) == 3
    assert len(bits) < bits.max_length


@pytest.mark.parametrize(
    "config",
    [
        dict(dir="left", value=0, res=[0, 0, 1, 0]),
        dict(dir="right", value=1, res=[0, 1, 0, 1]),
    ],
)
def test_bit_string_push(bits, config):
    if config["dir"] == "left":
        bits.push_left(Bit(config["value"]))
        assert len(bits) == 4
        assert len(bits) < bits.max_length
        for bit0, bit1 in zip(bits._bits, config["res"]):
            assert int(bool(bit0)) == bit1

    elif config["dir"] == "right":
        bits.push_right(Bit(config["value"]))
        assert len(bits) == 4
        assert len(bits) < bits.max_length
        for bit0, bit1 in zip(bits._bits, config["res"]):
            assert int(bool(bit0)) == bit1
