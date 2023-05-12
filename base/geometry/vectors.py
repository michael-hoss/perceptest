import math
from typing import Optional


class Quaternion(list[float]):
    def __init__(self, values=None, heading: Optional[float] = None):
        if values is None and heading is None:
            values = [1, 0, 0, 0]
        elif values is not None and heading is not None:
            raise ValueError("Cannot specify both values and heading_angle")
        elif heading is not None:
            # Compute quaternion from heading angle only according to
            # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
            q_w = math.cos(heading / 2)
            q_x = 0
            q_y = 0
            q_z = math.sin(heading / 2)  # heading rotation is about z axis
            values = [q_w, q_x, q_y, q_z]
        elif values:
            if not self.is_valid_rotation(values):
                raise ValueError("Invalid rotation format")

        super().__init__(values)

    @classmethod
    def is_valid_rotation(cls, value: list[float]) -> bool:
        if not isinstance(value, list):
            return False
        if len(value) != 4:
            return False
        return True


class Vector3(list[float]):
    def __init__(self, value=None):
        if value is None:
            value = [0, 0, 0]
        elif not self.is_valid_vector3(value):
            raise ValueError("Invalid Vector3 format")

        super().__init__(value)

    @classmethod
    def is_valid_vector3(cls, value: list[float]) -> bool:
        if not isinstance(value, list):
            return False
        if len(value) != 3:
            return False
        return True


class Vector2(list[float]):
    def __init__(self, value=None):
        if value is None:
            value = [0, 0]
        elif not self.is_valid_vector2(value):
            raise ValueError("Invalid Vector2 format")

        super().__init__(value)

    @classmethod
    def is_valid_vector2(cls, value: list[float]) -> bool:
        if not isinstance(value, list):
            return False
        if len(value) != 2:
            return False
        return True
