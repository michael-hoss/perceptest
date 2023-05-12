import sys

import pytest

from base.geometry.vectors import Quaternion, Vector3


def test_vector3_pass() -> None:
    vector = Vector3([0, 0, 0])
    vector_list: list = list(vector)
    assert isinstance(vector_list, list)


def test_vector3_default_init_pass() -> None:
    vector = Vector3()
    vector_list: list = list(vector)
    assert isinstance(vector_list, list)


def test_quaternion_pass() -> None:
    quaternion = Quaternion([1, 0, 0, 0])
    quaternion_list: list = list(quaternion)
    assert isinstance(quaternion_list, list)


def test_quaternion_default_init_pass() -> None:
    quaternion = Quaternion()
    quaternion_list: list = list(quaternion)
    assert isinstance(quaternion_list, list)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
