from constants import MIN_V, MAX_V, EPS

class InputError(Exception):
    # check with the accuracy value (zero check)
    def is_zero(z: float) -> bool:
        return abs(z) <= EPS

    # reading user input value
    def read_int(prompt: str) -> int:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError as e:
            raise InputError(f"ERROR: float value expected - "
                             f"value '{s}' has type missmatch / out of range [{MIN_V}; {MAX_V}].;") from e

    def validate_range(v: int, name: str) -> None:
        if v < MIN_V or v > MAX_V:
            raise InputError(f"ERROR: value {name}={v} out of range [{MIN_V}; {MAX_V}].; ")