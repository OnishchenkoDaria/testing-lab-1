from console_input import InputError, ConsoleInputReader
from console_output import print_result
from utils import line_from_two_points, line_from_kb, classify_three_lines


def main() -> int:
    try:
        inp = ConsoleInputReader.read_inputs()

        # Build lines
        l1 = line_from_two_points(inp.p11, inp.p12)
        l2 = line_from_two_points(inp.p21, inp.p22)
        l3 = line_from_kb(inp.k, inp.b)

        res = classify_three_lines(l1, l2, l3)
        print_result(res)

        return 0

    except InputError as e:
        print(str(e))
        return 2
    except KeyboardInterrupt:
        print("\nDiscarded by user.")
        return 130 # out of range boundaries
    except Exception as e:
        print(f"ERROR: {e}; Unrecognised error - check the input data according to the validation messages.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())