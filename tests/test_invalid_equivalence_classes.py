import pytest
from console_input import ConsoleInputReader, InputError
from schemas import Point


@pytest.mark.parametrize("value", [-121, 121, 999])
def test_out_of_range(value):
    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_range(value, "x")

    # assert correct exception type
    assert isinstance(exc_info.value, InputError)

    # check error message being up to the error case
    assert "range" in str(exc_info.value).lower()


@pytest.mark.parametrize("b", [0, 0, 0])
def test_b_zero_invalid(b):
    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_b_not_zero(b)

    assert isinstance(exc_info.value, InputError)
    assert exc_info.value.args
    assert "b" in exc_info.value.args[0].lower()
    assert "0" in exc_info.value.args[0]


@pytest.mark.parametrize("x,y", [
    (0, 0),
    (-120, -120),
    (120, 120),
])
def test_equal_points_invalid(x, y):
    p1 = Point(x, y)
    p2 = Point(x, y)

    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_two_points_not_equal(p1, p2, "L1")

    assert isinstance(exc_info.value, InputError)
    assert "equal" in str(exc_info.value).lower()