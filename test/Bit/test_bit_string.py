import pytest

from Computer.Bit import Bit, BitString
from Computer.Bit.bit import BitError


@pytest.fixture
def bits():
    bits: BitString = BitString(max_length=10)
    bits.push_right(Bit(0))
    bits.push_right(Bit(1))
    bits.push_right(Bit(0))
    return bits


def test_bit_string_init():
    empty: BitString = BitString(max_length=10)
    assert isinstance(empty._max_length, int)
    assert empty._max_length == 10
    assert isinstance(empty._bits, list)
    assert empty._bits == []


def test_bit_string_max_length(bits):
    assert bits.max_length == 10


def test_bit_string_getitem_error_out_of_bounds(bits):
    with pytest.raises(BitError) as exc:
        bits[4]

    assert exc.value.args[0] == "Index 4 lies outside the bit string length!"


def test_bit_string_getitem(bits):
    assert bits[0] == Bit(0)
    assert bits[1] == Bit(1)
    assert bits[2] == Bit(0)


def test_bit_string_iter(bits):
    res = [0, 1, 0]
    for bit0, bit1 in zip(bits, res):
        assert isinstance(bit0, Bit)
        assert bit0 == Bit(bit1)


def test_bit_string_length(bits):
    assert len(bits) == 3
    assert len(bits) < bits.max_length


def test_bit_string_extend_error_exceed_max_length():
    bits: BitString = BitString(max_length=1)
    bits._bits = [Bit(0)]

    stuff: BitString = BitString(max_length=10)
    stuff._bits = [Bit(1)]

    with pytest.raises(BitError) as exc:
        bits.extend_left(stuff)

    assert exc.value.args[0] == (
        "Adding 1 more bits to the bit string will exceed the max length!"
    )

    with pytest.raises(BitError) as exc:
        bits.extend_right(stuff)

    assert exc.value.args[0] == (
        "Adding 1 more bits to the bit string will exceed the max length!"
    )


@pytest.mark.parametrize(
    "config",
    [
        dict(dir="left", value=[0, 1], res=[0, 1, 0, 1, 0]),
        dict(dir="right", value=[1, 1], res=[0, 1, 0, 1, 1]),
    ],
)
def test_bit_string_extend(bits, config):
    stuff: BitString = BitString(max_length=2)
    stuff._bits = [Bit(val) for val in config["value"]]

    if config["dir"] == "left":
        bits.extend_left(stuff)
    elif config["dir"] == "right":
        bits.extend_right(stuff)

    assert len(bits) == 5
    for bit0, bit1 in zip(bits, config["res"]):
        assert bit0 == Bit(bit1)


def test_bit_string_pop_error_len_zero():
    bits: BitString = BitString(max_length=10)
    with pytest.raises(BitError) as exc:
        bits.pop_left()

    exc.value.args[0] == "This bit string is empty!"
    with pytest.raises(BitError) as exc:
        bits.pop_right()

    exc.value.args[0] == "This bit string is empty!"


@pytest.mark.parametrize(
    "config",
    [
        dict(dir="left", res=[0, 1, 0]),
        dict(dir="right", res=[0, 1, 0]),
    ],
)
def test_bit_string_pop(bits, config):
    while len(bits._bits) > 0:
        if config["dir"] == "left":
            bit: Bit = bits.pop_left()
            res: Bit = Bit(config["res"].pop(0))
            assert bit == res
        elif config["dir"] == "right":
            bit: Bit = bits.pop_right()
            res: Bit = Bit(config["res"].pop(-1))
            assert bit == res


def test_bit_string_push_error_exceed_max_length():
    bits: BitString = BitString(max_length=1)
    bits._bits = [Bit(0)]

    with pytest.raises(BitError) as exc:
        bits.push_left(Bit(0))

    assert exc.value.args[0] == (
        "This bit string has the maximum number of bits allowed!"
    )

    with pytest.raises(BitError) as exc:
        bits.push_right(Bit(1))

    assert exc.value.args[0] == (
        "This bit string has the maximum number of bits allowed!"
    )


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
    elif config["dir"] == "right":
        bits.push_right(Bit(config["value"]))

    assert len(bits) == 4
    assert len(bits) < bits.max_length
    for bit0, bit1 in zip(bits._bits, config["res"]):
        assert bit0 == Bit(bit1)
