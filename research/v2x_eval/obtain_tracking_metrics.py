import glob
import json
from os import path
from typing import Any

from nuscenes.eval.tracking.tooling.evaluate_tracking import (
    MetricsSummary,
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    nuscenes_devkit_tracking_eval,
)
from nuscenes.eval.tracking.tooling.nuscenes_format import TrackingEvalParams
from rich.progress import Progress  # type: ignore

from base.cli.suppress_stdout import suppress_output
from research.v2x_eval.constants import ConversionConfig


def obtain_metrics_for_nuscenes_version_dirs(conversion_config: ConversionConfig) -> dict[str, Any]:
    """Compute object tracking metrics for all directories under artery_logs_root_dir/NUSCENES_DIRNAME
    that have the given dirstem.

    Returns a dict
    {
        "simXXdata": metrics_of_all_splits_of_simXXdata,
        "simYYdata": metrics_of_all_splits_of_simYYdata,  # etc.
    }
    """
    pattern = path.join(conversion_config.nuscenes_root_dir, "sim??data")
    matching_dirs = glob.glob(pattern)
    matching_dirs = [dir for dir in sorted(matching_dirs) if path.isdir(dir)]

    metrics_of_configs: dict[str, Any] = {}

    with Progress(refresh_per_second=2) as progress:
        dir_task = progress.add_task("[blue]Obtaining nuScenes metrics...", total=len(matching_dirs))
        for artery_config in matching_dirs:
            metrics_of_splits: dict[str, Any] = obtain_metrics_for_all_splits(
                artery_config=artery_config,
                conversion_config=conversion_config,
                progress=progress,
            )
            metrics_of_configs[artery_config] = metrics_of_splits
            progress.update(dir_task, advance=1)
        return metrics_of_configs


def obtain_metrics_for_all_splits(
    artery_config: str,
    conversion_config: ConversionConfig,
    progress: Progress,
) -> dict[str, Any]:
    """Returns a dict mapping split names to metrics summary dicts, e.g.
    {
        "all": metrics_summary_dict_on_all_results_YY,
        "results_01": metrics_summary_dict_on_results_01,
        "results_02": metrics_summary_dict_on_results_01,  # etc
    }
    """
    splits_data: dict = {}
    custom_splits_path = conversion_config.get_splits_filename(artery_config)
    with open(custom_splits_path, "r") as file:
        splits_data = json.load(file)

    metrics_of_splits: dict[str, Any] = {}
    splits_task = progress.add_task(
        f"[green]Obtaining metrics in {path.basename(artery_config)}...", total=len(splits_data)
    )
    for split_name in splits_data.keys():
        metrics_of_splits[split_name] = obtain_metrics_for_split(
            artery_config, conversion_config=conversion_config, eval_split=split_name
        )
        progress.update(splits_task, advance=1, refresh=True)
    return metrics_of_splits


def obtain_metrics_for_split(
    artery_config: str, conversion_config: ConversionConfig, eval_split: str = "all"
) -> MetricsSummary:
    tracking_eval_params = TrackingEvalParams(
        result_path=conversion_config.get_tracking_result_path(artery_config=artery_config),
        output_dir=conversion_config.get_metrics_output_dir(artery_config, eval_split),
        eval_set=eval_split,  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot=conversion_config.nuscenes_root_dir,
        nusc_version=artery_config,
    )

    if not conversion_config.force_regenerate and metrics_files_present_on_disk(tracking_eval_params):
        return read_metrics_from_disk(tracking_eval_params)

    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(
        config_path=conversion_config.nuscenes_eval_config_path
    )
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
