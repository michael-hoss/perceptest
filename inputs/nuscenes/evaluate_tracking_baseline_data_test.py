import sys
import tempfile

import pytest
from nuscenes.eval.tracking.tooling.evaluate_tracking import (
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    get_official_tracking_config,
    nuscenes_devkit_tracking_eval,
)
from nuscenes.eval.tracking.tooling.nuscenes_format import TrackingEvalParams

"""
These tests merely document the original baseline usage of the nuscenes devkit evaluation.
Since the evaluation gets called on the original dataset and baseline submission, which are quite 
large, evaluation can take quite long (e.g. 10mins).
"""


@pytest.fixture
def official_config_stripped_path():
    return "inputs/nuscenes/official_config_stripped.json"


@pytest.fixture
def custom_config_path():
    return "inputs/nuscenes/example_custom_config.json"


@pytest.fixture
def baseline_eval_params():
    return TrackingEvalParams(
        result_path="/data/sets/tracking-megvii/results_val_megvii.json",
        output_dir=tempfile.mkdtemp(prefix="tracking_eval_outputs_val_"),
        eval_set="val",  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot="/data/sets/nuscenes",
        nusc_version="v1.0-trainval",
    )


def test_get_nuscenes_tracking_config_from_own_file_pass(custom_config_path: str) -> None:
    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(config_path=custom_config_path)
    assert config is not None
    assert config.dist_fcn == "center_distance"


def test_nuscenes_devkit_tracking_eval_baseline_stripped_pass(
    baseline_eval_params: TrackingEvalParams, official_config_stripped_path: str
) -> None:
    """This only works if the lidarseg directory is also present in the nuscenes root dir!"""
    config = get_nuscenes_tracking_config_from_own_file(config_path=official_config_stripped_path)
    metrics_summary = nuscenes_devkit_tracking_eval(params=baseline_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


def test_nuscenes_devkit_tracking_eval_baseline_stripped_custom_split_pass(official_config_stripped_path: str) -> None:
    custom_split_trainval_eval_params = TrackingEvalParams(
        result_path="/data/sets/tracking-megvii/results_val_megvii.json",
        output_dir=tempfile.mkdtemp(prefix="tracking_eval_outputs_val_"),
        eval_set="mini_custom_val",
        nusc_dataroot="/data/sets/nuscenes",
        nusc_version="v1.0-trainval",
    )
    config = get_nuscenes_tracking_config_from_own_file(config_path=official_config_stripped_path)
    metrics_summary = nuscenes_devkit_tracking_eval(params=custom_split_trainval_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


@pytest.mark.fail()
def test_nuscenes_devkit_tracking_eval_baseline_stripped_custom_split_mini_fail(
    official_config_stripped_path: str,
) -> None:
    """This test fails because the file in result_path contains samples that are not in nusc_version."""
    custom_split_mini_eval_params = TrackingEvalParams(
        result_path="/data/sets/tracking-megvii/results_val_megvii.json",  # note that this contains results for val, not for mini
        output_dir=tempfile.mkdtemp(prefix="tracking_eval_outputs_val_"),
        eval_set="mini_custom_val",  # mini_custom_val is a subset of both val and mini
        nusc_dataroot="/data/sets/nuscenes",
        nusc_version="v1.0-mini",  # Note that we try to evaluate on mini
    )
    config = get_nuscenes_tracking_config_from_own_file(config_path=official_config_stripped_path)
    metrics_summary = nuscenes_devkit_tracking_eval(params=custom_split_mini_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


@pytest.mark.skip()
def test_nuscenes_devkit_tracking_eval_baseline_full_pass(baseline_eval_params: TrackingEvalParams) -> None:
    config: TrackingConfig = get_official_tracking_config()
    metrics_summary = nuscenes_devkit_tracking_eval(params=baseline_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
