import pytest
from console_input import ConsoleInputReader, InputError
from schemas import Point
from constants import MIN_V, MAX_V


@pytest.mark.parametrize("value", [MIN_V - 1, MAX_V + 1, 999, -999])
def test_out_of_range(value):
    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_range(value, "x")

    msg = str(exc_info.value).lower()
    assert "out of range" in msg
    assert "fix:" in msg


@pytest.mark.parametrize("b", [0])
def test_b_zero_invalid(b):
    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_b_not_zero(b)

    msg = str(exc_info.value).lower()
    assert "b equals 0" in msg or "b!=0" in msg
    assert "fix:" in msg


@pytest.mark.parametrize("x,y", [
    (0, 0),
    (MIN_V, MIN_V),
    (MAX_V, MAX_V),
])
def test_equal_points_invalid(x, y):
    p1 = Point(x, y)
    p2 = Point(x, y)

    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.validate_two_points_not_equal(p1, p2, "L1")

    msg = str(exc_info.value).lower()

    assert "identical" in msg and "points" in msg
    assert "fix:" in msg


def test_read_int_rejects_text(monkeypatch):
   # not numeric, input data type missmatch
    monkeypatch.setattr("builtins.input", lambda _: "hello")

    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.read_int("x = ")

    msg = str(exc_info.value).lower()
    assert "integer value expected" in msg
    assert "fix:" in msg


def test_read_int_rejects_float_string(monkeypatch):
    # integer inputs, not float
    monkeypatch.setattr("builtins.input", lambda _: "3.14")

    with pytest.raises(InputError) as exc_info:
        ConsoleInputReader.read_int("x = ")

    msg = str(exc_info.value).lower()
    assert "integer value expected" in msg
    assert "fix:" in msg