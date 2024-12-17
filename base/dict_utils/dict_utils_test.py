import sys

import pytest

from base.dict_utils.dict_utils import remove_key_recursively


def test_remove_key_recursively() -> None:
    original_dict = {
        "name": "Alice",
        "age": 30,
        "address": {"city": "Wonderland", "postal_code": "12345"},
        "email": "alice@example.com",
        "preferences": {"color": "blue", "notifications": {"email": True, "sms": False}},
    }

    expected_output = {
        "name": "Alice",
        "age": 30,
        "address": {"city": "Wonderland", "postal_code": "12345"},
        "preferences": {"color": "blue", "notifications": {"sms": False}},
    }
    new_dict = remove_key_recursively(original_dict=original_dict, key_to_remove="email")
    assert sorted(new_dict) == sorted(expected_output)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
