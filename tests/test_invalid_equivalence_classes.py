import pytest
from console_input import ConsoleInputReader, InputError
from schemas import Point


@pytest.mark.parametrize("value", [-121, 121, 999])
def test_out_of_range(value):
    with pytest.raises(InputError):
        ConsoleInputReader.validate_range(value, "x")


@pytest.mark.parametrize("b", [0, 0, 0])
def test_b_zero_invalid(b):
    with pytest.raises(InputError):
        ConsoleInputReader.validate_b_not_zero(b)


@pytest.mark.parametrize("x,y", [
    (0, 0),
    (-120, -120),
    (120, 120),
])
def test_equal_points_invalid(x, y):
    p1 = Point(x, y)
    p2 = Point(x, y)

    with pytest.raises(InputError):
        ConsoleInputReader.validate_two_points_not_equal(p1, p2, "L1")