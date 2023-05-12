import sys

import pytest

from base.geometry.vectors import Quaternion, Vector3
from inputs.nuscenes.nuscenes_format import Attribute, CalibratedSensor, Guid


def test_attribute_as_dict_pass() -> None:
    attribute = Attribute(token=Guid(), name="vehicle.moving", description="Vehicle is moving.")
    attribute_dict = attribute.to_dict()
    assert isinstance(attribute_dict, dict)
    assert "token" in attribute_dict
    assert "name" in attribute_dict
    assert "description" in attribute_dict
    assert "json_filename" not in attribute_dict


def test_calibrated_sensor_as_dict_pass() -> None:
    calibrated_sensor = CalibratedSensor(
        token=Guid(),
        sensor_token=Guid(),
        translation=Vector3([0, 0, 0]),
        rotation=Quaternion([1, 0, 0, 0]),
        camera_intrinsic=[],
    )

    calibrated_sensor_dict = calibrated_sensor.to_dict()
    assert isinstance(calibrated_sensor_dict, dict)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
