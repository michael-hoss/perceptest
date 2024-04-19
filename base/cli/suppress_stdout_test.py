import sys
from io import StringIO

import pytest

from base.cli.suppress_stdout import suppress_output


def capture_stdout(func, *args, **kwargs):
    # Create a StringIO object to capture stdout
    stdout_capture = StringIO()
    sys.stdout = stdout_capture

    # Call the function with the provided arguments
    func(*args, **kwargs)

    # Reset sys.stdout to its original value
    sys.stdout = sys.__stdout__

    # Return the captured stdout
    return stdout_capture.getvalue()


def example_function_that_outputs_stuff():
    print("stuff")


def example_function_that_is_suppressed():
    with suppress_output():
        example_function_that_outputs_stuff()


def test_suppress_output_pass() -> None:
    assert capture_stdout(example_function_that_outputs_stuff) == "stuff\n"
    assert capture_stdout(example_function_that_is_suppressed) == ""


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
