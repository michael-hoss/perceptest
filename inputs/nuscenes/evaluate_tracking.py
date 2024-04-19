import json
import os
from typing import Optional

from nuscenes.eval.tracking.evaluate import TrackingConfig, TrackingEval, config_factory

from inputs.nuscenes.nuscenes_format import MetricsSummary, TrackingEvalParams

"""This is a wrapper around the nuscenes devkit tracking eval function.
Like this, I can call my own function and don't have to use their interface in the rest of my code."""


def get_nuscenes_tracking_config_from_own_file(config_path: str) -> TrackingConfig:
    """Get the nuscenes tracking config from a file in the repo.

    Args:
        config_path: The path to the file relative to the perceptest repo root.
    """

    current_file_path = os.path.abspath(__file__)
    current_dir_path = os.path.dirname(current_file_path)
    abs_config_path = os.path.join(current_dir_path, "../..", config_path)
    abs_config_path = os.path.abspath(abs_config_path)
    with open(abs_config_path, "r") as _f:
        return TrackingConfig.deserialize(json.load(_f))  # type: ignore


def get_official_tracking_config() -> TrackingConfig:
    config = config_factory("tracking_nips_2019")
    return config  # type: ignore


def nuscenes_devkit_tracking_eval(
    params: TrackingEvalParams, config: Optional[TrackingConfig] = None
) -> MetricsSummary:
    config = config or get_official_tracking_config()

    tracking_eval_object = TrackingEval(
        config=config,
        result_path=params.result_path,
        output_dir=params.output_dir,
        eval_set=params.eval_set,
        nusc_dataroot=params.nusc_dataroot,
        nusc_version=params.nusc_version,
        verbose=params.verbose,
        render_classes=params.render_classes,  # type: ignore
    )
    # If we don't want the file io, we can also just call .evaluate() on the tracking_eval_object
    metrics_summary: MetricsSummary = tracking_eval_object.main()
    return metrics_summary
