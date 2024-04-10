import json
from os import path
from typing import Any

from inputs.nuscenes.evaluate_tracking import (
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    nuscenes_devkit_tracking_eval,
)
from inputs.nuscenes.nuscenes_format import TrackingEvalParams
from research.v2x_eval.constants import (
    NUSCENES_DATAROOT,
    NUSCENES_EVAL_CONFIG_PATH,
    NUSCENES_METRICS_OUTPUT_DIR,
    NUSCENES_OUT_RESULTS_FILE,
)


def compute_metrics_for_all_splits(nuscenes_dump_dir: str) -> dict[str, Any]:
    splits_data: dict = {}
    custom_splits_path = path.join(nuscenes_dump_dir, "splits.json")
    with open(custom_splits_path, "r") as file:
        splits_data = json.load(file)

    for split_name in splits_data.keys():
        metrics_summary: dict[str, Any] = compute_metrics_for_split(nuscenes_dump_dir, eval_split=split_name)
    return metrics_summary


def compute_metrics_for_split(nuscenes_dump_dir: str, eval_split: str = "all") -> dict[str, Any]:
    tracking_eval_params = TrackingEvalParams(
        result_path=path.join(nuscenes_dump_dir, NUSCENES_OUT_RESULTS_FILE),
        output_dir=path.join(nuscenes_dump_dir, NUSCENES_METRICS_OUTPUT_DIR, eval_split),
        eval_set=eval_split,  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot=NUSCENES_DATAROOT,
        nusc_version=nuscenes_dump_dir,
    )

    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(config_path=NUSCENES_EVAL_CONFIG_PATH)
    metrics_summary: dict[str, Any] = nuscenes_devkit_tracking_eval(params=tracking_eval_params, config=config)
    return metrics_summary
