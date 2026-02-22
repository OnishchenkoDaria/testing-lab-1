from constants import MIN_V, MAX_V, EPS
from schemas import Point, Inputs


class InputError(Exception):
    pass


class ConsoleInputReader:

    # reading user input value
    @staticmethod
    def read_int(prompt: str) -> int:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError as e:
            raise InputError(
                f"ERROR: int value expected - value '{s}' has type mismatch / "
                f"out of range [{MIN_V}; {MAX_V}]."
            ) from e

    @staticmethod
    def validate_range(v: int, name: str) -> None:
        if v < MIN_V or v > MAX_V:
            raise InputError(
                f"ERROR: value {name}={v} out of range [{MIN_V}; {MAX_V}]."
            )

    @staticmethod
    def validate_two_points_not_equal(p1: Point, p2: Point, which: str) -> None:
        # checking for duplicate points
        # using exact equality here because default input is integer
        if int(p1.x) == int(p2.x) and int(p1.y) == int(p2.y):
            raise InputError(
                f"ERROR: for {which} - two equal points ({int(p1.x)},{int(p1.y)}). "
                f"Should satisfy (x1-x2)^2+(y1-y2)^2 != 0."
            )

    @staticmethod
    def validate_b_not_zero(b: int) -> None:
        if b == 0:
            raise InputError(
                "ERROR: for y=kx+b parameter b equals to 0 (b != 0 required)."
            )

    def read_inputs(self) -> Inputs:
        print("Enter 3 sets of parameters")
        print(f"Integer numbers in range [{MIN_V}; {MAX_V}].")

        print("L1: two points (x11,y11) & (x12,y12)")
        x11 = self.read_int("x11 = ")
        y11 = self.read_int("y11 = ")
        x12 = self.read_int("x12 = ")
        y12 = self.read_int("y12 = ")

        print("L2: two points (x21,y21) & (x22,y22)")
        x21 = self.read_int("x21 = ")
        y21 = self.read_int("y21 = ")
        x22 = self.read_int("x22 = ")
        y22 = self.read_int("y22 = ")

        print("L3: y = kx + b (b != 0)")
        k = self.read_int("k = ")
        b = self.read_int("b = ")

        # range validation for all
        for name, v in [
            ("x11", x11), ("y11", y11), ("x12", x12), ("y12", y12),
            ("x21", x21), ("y21", y21), ("x22", x22), ("y22", y22),
            ("k", k), ("b", b)
        ]:
            self.validate_range(v, name)

        p11 = Point(float(x11), float(y11))
        p12 = Point(float(x12), float(y12))
        p21 = Point(float(x21), float(y21))
        p22 = Point(float(x22), float(y22))

        self.validate_two_points_not_equal(p11, p12, "L1")
        self.validate_two_points_not_equal(p21, p22, "L2")
        self.validate_b_not_zero(b)

        return Inputs(p11=p11, p12=p12, p21=p21, p22=p22, k=k, b=b)