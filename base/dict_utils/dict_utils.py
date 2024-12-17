from typing import Any


def remove_key_recursively(original_dict: Any, key_to_remove: str, input_type: type = dict):
    """
    Recursively removes a key from a dictionary, including nested dictionaries.
    """

    new_dict = {}
    for key, value in original_dict.items():
        if key == key_to_remove:
            continue

        if isinstance(value, dict) or isinstance(value, input_type):
            value = remove_key_recursively(value, key_to_remove, input_type)
        new_dict[key] = value

    return new_dict
