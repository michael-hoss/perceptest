import os
import sys

import pytest

from inputs.nuscenes.evaluate_tracking import (
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    get_official_tracking_config,
)


@pytest.fixture
def artery_config_path():
    return "inputs/artery/to_nuscenes/artery_config_for_nuscenes.json"


@pytest.mark.skip
def test_python_path_was_properly_set_in_bazel_rule() -> None:
    python_path = os.environ.get("PYTHONPATH", "").split(":")
    python_path = [path.split(".runfiles/")[-1] for path in python_path]
    print("PYTHONPATH:", python_path)
    # The path to nuscenes-devkit/python-sdk should be included s.th. the interpreter finds
    # imports like: `from nuscenes.xyz import abc`


def test_get_nuscenes_tracking_config_from_own_file_pass(artery_config_path: str) -> None:
    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(config_path=artery_config_path)
    assert config is not None
    assert config.dist_fcn == "center_distance"


def test_get_official_tracking_config_pass() -> None:
    config: TrackingConfig = get_official_tracking_config()
    assert config is not None
    assert config.dist_fcn == "center_distance"
    assert "bicycle" in config.class_names


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
