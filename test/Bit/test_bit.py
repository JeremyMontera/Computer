import pytest
from Computer.Bit import Bit
from Computer.Bit.bit import BitError

@pytest.mark.parametrize(
    "config",
    [
        dict(value = 0, result = False),
        dict(value = 1, result = True),
        dict(value = '0', result = False),
        dict(value = '1', result = True),
        dict(value = False, result = False),
        dict(value = True, result = True),
    ]
)
def test_bit_creation(config):
    bit = Bit(config["value"])
    assert bool(bit) == config["result"]

def test_bit_creation_error_bad_input():
    with pytest.raises(BitError) as exc:
        Bit(2)

    assert exc.value.args[0] == "Entered an unknown value: 2!"
    with pytest.raises(BitError) as exc:
        Bit(['1'])

    assert exc.value.args[0] == "Entered something that cannot be handled!"