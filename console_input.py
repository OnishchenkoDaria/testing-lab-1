from constants import MIN_V, MAX_V
from schemas import Point, Inputs


class InputError(Exception):
    pass


class ConsoleInputReader:
    @staticmethod
    def _try_parse_int(raw: str) -> int:
        try:
            return int(raw)
        except ValueError as e:
            raise InputError(
                f"ERROR: integer value expected, got '{raw}'.; "
                f"Fix: enter an integer in range [{MIN_V}; {MAX_V}]."
            ) from e

    @staticmethod
    def validate_range(v: int, name: str) -> None:
        if v < MIN_V or v > MAX_V:
            raise InputError(
                f"ERROR: {name}={v} is out of range [{MIN_V}; {MAX_V}].; "
                f"Fix: enter {name} within [{MIN_V}; {MAX_V}]."
            )

    @staticmethod
    def validate_two_points_not_equal(p1: Point, p2: Point, which: str) -> None:
        # validate that two points are not identical
        # using exact equality because inputs are integers.
        if int(p1.x) == int(p2.x) and int(p1.y) == int(p2.y):
            raise InputError(
                f"ERROR: {which} has two identical points ({int(p1.x)},{int(p1.y)}).; "
                f"Fix: enter two different points so (x1-x2)^2+(y1-y2)^2 != 0."
            )

    @staticmethod
    def validate_b_not_zero(b: int) -> None:
        if b == 0:
            raise InputError(
                "ERROR: parameter b equals 0 for line y=kx+b, but b!=0 is required.; "
                "Fix: enter any non-zero integer value for b."
            )

    def read_int_in_range(self, name: str, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                v = self._try_parse_int(raw)
                self.validate_range(v, name)
                return v
            except InputError as e:
                print(e)  # diagnostic message: "ERROR; Fix"
                print("Please try again.")

    def read_b_non_zero(self, prompt: str = "b = ") -> int:
        while True:
            b = self.read_int_in_range("b", prompt)
            try:
                self.validate_b_not_zero(b)
                return b
            except InputError as e:
                print(e)
                print("Please try again.")

    def read_inputs(self) -> Inputs:
        print("Enter parameters for 3 lines (variant 20: 2,2,5).")
        print(f"All values must be integers in range [{MIN_V}; {MAX_V}].")
        print("L1: two points (x11,y11) and (x12,y12)")

        x11 = self.read_int_in_range("x11", "x11 = ")
        y11 = self.read_int_in_range("y11", "y11 = ")
        x12 = self.read_int_in_range("x12", "x12 = ")
        y12 = self.read_int_in_range("y12", "y12 = ")

        print("L2: two points (x21,y21) and (x22,y22)")
        x21 = self.read_int_in_range("x21", "x21 = ")
        y21 = self.read_int_in_range("y21", "y21 = ")
        x22 = self.read_int_in_range("x22", "x22 = ")
        y22 = self.read_int_in_range("y22", "y22 = ")

        print("L3: y = kx + b (b != 0)")
        k = self.read_int_in_range("k", "k = ")
        b = self.read_b_non_zero("b = ")

        p11 = Point(float(x11), float(y11))
        p12 = Point(float(x12), float(y12))
        p21 = Point(float(x21), float(y21))
        p22 = Point(float(x22), float(y22))

        self.validate_two_points_not_equal(p11, p12, "L1")
        self.validate_two_points_not_equal(p21, p22, "L2")

        return Inputs(p11=p11, p12=p12, p21=p21, p22=p22, k=k, b=b)