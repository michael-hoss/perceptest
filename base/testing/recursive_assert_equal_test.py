import re
import sys
from copy import deepcopy

import pytest

from base.testing.recursive_assert_equal import SKIP_TEST_HINT, assert_equal


def test_assert_equal_pass():
    expected = {
        "hey": "yeah",
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6668]},
        ],
    }
    actual = deepcopy(expected)

    assert_equal(expected=expected, actual=actual)


def test_assert_equal_fail_float():
    expected = {
        "hey": "yeah",
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6668]},
        ],
    }
    actual = {
        "hey": "yeah",
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6669]},
        ],
    }

    with pytest.raises(AssertionError, match=re.escape("Floats not equal ['otherkey', 1, 'c', 2]")):
        assert_equal(expected=expected, actual=actual)


def test_assert_equal_pass_mutated():
    expected = {
        "hey": "yeah",
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6668]},
        ],
    }
    actual = {
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6668]},
        ],
        "hey": "yeah",
    }

    assert_equal(expected=expected, actual=actual)


def test_assert_equal_pass_skiptest():
    expected = {
        "hey": "yeah",
        "otherkey": SKIP_TEST_HINT,
    }
    actual = {
        "hey": "yeah",
        "otherkey": [
            "string1",
            {"a": 1, "b": 2, "c": [4, 5, 6.6668]},
        ],
    }

    assert_equal(expected=expected, actual=actual)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
