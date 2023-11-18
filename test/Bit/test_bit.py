import pytest

from Computer.Bit import Bit
from Computer.Bit.bit import BitError


@pytest.mark.parametrize(
    "config",
    [
        dict(value=0, result=Bit(0)),
        dict(value=1, result=Bit(1)),
        dict(value="0", result=Bit(0)),
        dict(value="1", result=Bit(1)),
        dict(value=False, result=Bit(0)),
        dict(value=True, result=Bit(1)),
    ],
)
def test_bit_creation(config):
    bit = Bit(config["value"])
    assert bit == config["result"]


def test_bit_creation_error_bad_input():
    with pytest.raises(BitError) as exc:
        Bit(2)

    assert exc.value.args[0] == "Entered an unknown value: 2!"
    with pytest.raises(BitError) as exc:
        Bit(["1"])

    assert exc.value.args[0] == "Entered something that cannot be handled!"

@pytest.mark.parametrize(
    ("bits", "res"),
    [
        (
            [Bit(0), Bit(0)],
            [Bit(0), Bit(1), Bit(0)],
        ),
        (
            [Bit(0), Bit(1)],
            [Bit(0), Bit(1), Bit(1)],
        ),
        (
            [Bit(1), Bit(0)],
            [Bit(0), Bit(0), Bit(1)],
        ),
        (
            [Bit(1), Bit(1)],
            [Bit(1), Bit(0), Bit(1)],
        ),
    ],
)
def test_bit_op(bits, res):
    assert bits[0].and_op(bits[1]) == res[0]
    assert bits[0].not_op() == res[1]
    assert bits[0].or_op(bits[1]) == res[2]
