import glob
import json
from os import path
from re import findall
from typing import Any

from rich.progress import Progress  # type: ignore

from base.cli.suppress_stdout import suppress_output
from inputs.nuscenes.evaluate_tracking import (
    MetricsSummary,
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


def obtain_metrics_for_nuscenes_version_dirs(
    nuscenes_version_dirstem: str, force_regenerate: bool = False
) -> dict[str, Any]:
    """Compute object tracking metrics for all directories under NUSCENES_DATAROOT that have the given dirstem.

    Returns a dict
    {
        "simXXdata": metrics_of_all_splits_of_simXXdata,
        "simYYdata": metrics_of_all_splits_of_simYYdata,  # etc.
    }
    """
    pattern = path.join(NUSCENES_DATAROOT, nuscenes_version_dirstem + "_*/")
    matching_dirs = glob.glob(pattern)
    matching_dirs = [dir for dir in sorted(matching_dirs) if path.isdir(dir)]

    metrics_of_configs: dict[str, Any] = {}

    with Progress(refresh_per_second=2) as progress:
        dir_task = progress.add_task("[blue]Computing metrics for nuScenes dirs...", total=len(matching_dirs))
        for matching_dir in matching_dirs:
            config_name = findall(r"sim\d{2}data", matching_dir)[0]

            metrics_of_splits: dict[str, Any] = obtain_metrics_for_all_splits(
                nuscenes_dump_dir=matching_dir, force_regenerate=force_regenerate
            )
            metrics_of_configs[config_name] = metrics_of_splits
            progress.update(dir_task, advance=1)
        return metrics_of_configs


def obtain_metrics_for_all_splits(nuscenes_dump_dir: str, force_regenerate: bool = False) -> dict[str, Any]:
    """Returns a dict mapping split names to metrics summary dicts, e.g.
    {
        "all": metrics_summary_dict_on_all_results_YY,
        "results_01": metrics_summary_dict_on_results_01,
        "results_02": metrics_summary_dict_on_results_01,  # etc
    }
    """
    splits_data: dict = {}
    custom_splits_path = path.join(nuscenes_dump_dir, "splits.json")
    with open(custom_splits_path, "r") as file:
        splits_data = json.load(file)

    metrics_of_splits: dict[str, Any] = {}
    for split_name in splits_data.keys():
        metrics_of_splits[split_name] = obtain_metrics_for_split(
            nuscenes_dump_dir, eval_split=split_name, force_regenerate=force_regenerate
        )
    return metrics_of_splits


def obtain_metrics_for_split(
    nuscenes_dump_dir: str, eval_split: str = "all", force_regenerate: bool = False
) -> MetricsSummary:
    tracking_eval_params = TrackingEvalParams(
        result_path=path.join(nuscenes_dump_dir, NUSCENES_OUT_RESULTS_FILE),
        output_dir=path.join(nuscenes_dump_dir, NUSCENES_METRICS_OUTPUT_DIR, eval_split),
        eval_set=eval_split,  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot=NUSCENES_DATAROOT,
        nusc_version=path.basename(path.normpath(nuscenes_dump_dir)),
    )

    if not force_regenerate and metrics_files_present_on_disk(tracking_eval_params):
        return read_metrics_from_disk(tracking_eval_params)

    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(config_path=NUSCENES_EVAL_CONFIG_PATH)
    with suppress_output():
        metrics_summary: MetricsSummary = nuscenes_devkit_tracking_eval(params=tracking_eval_params, config=config)
    return metrics_summary


def metrics_files_present_on_disk(tracking_eval_params: TrackingEvalParams) -> bool:
    details_file: str = path.join(tracking_eval_params.output_dir, "metrics_details.json")
    summary_file: str = path.join(tracking_eval_params.output_dir, "metrics_summary.json")
    plots_dir: str = path.join(tracking_eval_params.output_dir, "plots")
    summary_plot: str = path.join(plots_dir, "summary.pdf")
    return (
        path.isfile(details_file) and path.isfile(summary_file) and path.isdir(plots_dir) and path.isfile(summary_plot)
    )


def read_metrics_from_disk(tracking_eval_params: TrackingEvalParams) -> MetricsSummary:
    summary_file: str = path.join(tracking_eval_params.output_dir, "metrics_summary.json")
    with open(summary_file, "r") as file:
        metrics_summary_from_disk = json.load(file)
        assert isinstance(metrics_summary_from_disk, dict)
    return metrics_summary_from_disk
