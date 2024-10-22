import math
from typing import Any

SKIP_TEST_HINT = "$SKIP_TEST"


def assert_equal_dicts(expected: dict, actual: dict, call_stack: list) -> None:
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        raise AssertionError("At least one value is not a dict", call_stack)

    if sorted(expected.keys()) != sorted(actual.keys()):
        raise AssertionError(
            "Keys don't match", call_stack, f"EXPECTED={sorted(expected.keys())}", f"ACTUAL={sorted(actual.keys())}"
        )

    for key in expected:
        call_stack.append(key)
        assert_equal(expected=expected[key], actual=actual[key], call_stack=call_stack)
        call_stack.pop()


def assert_equal_lists(expected: list, actual: list, call_stack: list) -> None:
    if not isinstance(expected, list) or not isinstance(actual, list):
        raise AssertionError("At least one value is not a list", call_stack)

    if len(expected) != len(actual):
        raise AssertionError("Lengths of lists don't match", call_stack)

    list_element = 0
    for expected_val, actual_val in zip(expected, actual):
        call_stack.append(list_element)
        list_element = list_element + 1
        assert_equal(expected_val, actual_val, call_stack)
        call_stack.pop()


def assert_equal(expected: Any, actual: Any, call_stack: list = []) -> None:
    """call_stack should be empty when used as the entry point for recursive equality checking."""

    if expected == SKIP_TEST_HINT:
        return

    if isinstance(expected, dict):
        assert_equal_dicts(expected, actual, call_stack)
    elif isinstance(expected, list):
        assert_equal_lists(expected, actual, call_stack)
    elif isinstance(expected, float):
        assert math.isclose(expected, actual), f"Floats not equal {call_stack}, {expected} vs. {actual}"
    else:
        assert expected == actual, f"Plain values not equal {call_stack}, {expected} vs. {actual}"
