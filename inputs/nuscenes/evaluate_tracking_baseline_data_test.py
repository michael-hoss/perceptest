import sys
import tempfile

import pytest

from inputs.nuscenes.evaluate_tracking import (
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    get_official_tracking_config,
    nuscenes_devkit_tracking_eval,
)
from inputs.nuscenes.nuscenes_format import TrackingEvalParams


@pytest.fixture
def official_config_stripped_path():
    return "inputs/nuscenes/official_config_stripped.json"


@pytest.fixture
def baseline_eval_params():
    return TrackingEvalParams(
        result_path="/data/sets/tracking-megvii/results_val_megvii.json",
        output_dir=tempfile.mkdtemp(prefix="tracking_eval_outputs_val_"),
        eval_set="val",  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot="/data/sets/nuscenes",
        nusc_version="v1.0-trainval",
    )


def test_nuscenes_devkit_tracking_eval_baseline_stripped_pass(
    baseline_eval_params: TrackingEvalParams, official_config_stripped_path: str
) -> None:
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
def test_nuscenes_devkit_tracking_eval_baseline_stripped_custom_split_mini_pass(
    official_config_stripped_path: str,
) -> None:
    """This test fails because the file in result_path contains samples that are not in nusc_version."""
    custom_split_mini_eval_params = TrackingEvalParams(
        result_path="/data/sets/tracking-megvii/results_val_megvii.json",  # note that this contains results for val
        output_dir=tempfile.mkdtemp(prefix="tracking_eval_outputs_val_"),
        eval_set="mini_custom_val",  # mini_custom_val is a subset of both val and mini
        nusc_dataroot="/data/sets/nuscenes",
        nusc_version="v1.0-mini",  # Note that we try to evaluate on mini
    )
    config = get_nuscenes_tracking_config_from_own_file(config_path=official_config_stripped_path)
    metrics_summary = nuscenes_devkit_tracking_eval(params=custom_split_mini_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


def test_nuscenes_devkit_tracking_eval_baseline_full_pass(baseline_eval_params: TrackingEvalParams) -> None:
    config: TrackingConfig = get_official_tracking_config()
    metrics_summary = nuscenes_devkit_tracking_eval(params=baseline_eval_params, config=config)
    assert isinstance(metrics_summary, dict)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
