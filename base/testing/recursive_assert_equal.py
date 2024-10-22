import math
from typing import Any


def assert_equal(expected: Any, actual: Any) -> None:
    if isinstance(expected, dict):
        assert_equal_dicts(expected, actual)
    elif isinstance(expected, list):
        assert_equal_lists(expected, actual)
    elif isinstance(expected, float):
        assert math.isclose(expected, actual), "Floats not equal"
    else:
        assert expected == actual, "Plain values not equal"


def assert_equal_dicts(expected: dict, actual: dict) -> None:
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        raise AssertionError("At least one value is not a dict")

    if sorted(expected.keys()) != sorted(actual.keys()):
        raise AssertionError("Keys don't match")

    for key in expected:
        assert_equal(expected=expected[key], actual=actual[key])


def assert_equal_lists(expected: list, actual: list) -> None:
    if not isinstance(expected, list) or not isinstance(actual, list):
        raise AssertionError("At least one value is not a list")

    if len(expected) != len(actual):
        raise AssertionError("Lengths of lists don't match")

    for expected_val, actual_val in zip(expected, actual):
        assert_equal(expected_val, actual_val)
