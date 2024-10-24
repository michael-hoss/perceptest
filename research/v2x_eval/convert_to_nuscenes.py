import glob
import re
from os import path
from typing import TYPE_CHECKING

from nuscenes.eval.tracking.tooling.custom_data_eval_config import CustomDataEvalConfig
from nuscenes.eval.tracking.tooling.nuscenes_format import NuScenesAll
from nuscenes.eval.tracking.tooling.nuscenes_format_utils import dump_to_nuscenes_dir, merge_nuscenes_all
from rich.progress import Progress, TaskID  # type: ignore

from inputs.artery.artery_format import ArterySimLogDump
from inputs.artery.from_logs.main_loader import pull_artery_sim_log
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArterySimLog

"""
This file applies the utils for conversion to the nuscenes json format. 

The code under `inputs/artery/to_nuscenes` converts *one* ArterySimLog to the nuScenes classes.
In contrast, the code here handles conversion of *many* ArterySimLog using custom splits.

The actual input data is unimportant; it just serves as an example to showcase the conversion.
"""


def convert_to_nuscenes_version_dirs(eval_config: CustomDataEvalConfig) -> None:
    """
    - creates custom nuscenes dataset versions for each match of eval_config.subdir_pattern (e.g. simXXdata)
    - makes each individual sub-subdir ("results_YY") a separate scene within "simXXdata"
    - creates custom splits
        - for each individual results_YY ("results_YY")
        - for all results_YY combined ("all")
    """
    with Progress(refresh_per_second=1) as progress:
        artery_log_dirs: dict = get_structured_artery_log_dirs(eval_config)
        configs_task = progress.add_task(
            "[blue]Obtaining nuScenes files from artery logs...", total=len(artery_log_dirs)
        )
        for artery_config_name, artery_iteration_names in artery_log_dirs.items():
            # Potentially skip if the nuscenes version directory already exists
            if not eval_config.force_regenerate and path.exists(
                eval_config.get_nuscenes_version_dir(artery_config_name)
            ):
                progress.update(configs_task, advance=1)
                continue

            convert_artery_config_logs_to_nuscenes_dir(
                conversion_config=eval_config,
                progress=progress,
                configs_task=configs_task,
                artery_config_name=artery_config_name,
                artery_iteration_names=artery_iteration_names,
            )


def convert_artery_config_logs_to_nuscenes_dir(
    conversion_config: CustomDataEvalConfig,
    progress: Progress,
    configs_task: TaskID,
    artery_config_name: str,
    artery_iteration_names: list[str],
):
    iterations_task = progress.add_task("", total=len(artery_iteration_names))
    nuscenes_all_list: list[NuScenesAll] = []

    # Convert each artery config iteration to a NuScenesAll instance
    for artery_iteration_name in artery_iteration_names:
        progress.update(
            iterations_task, description=f"[green]Converting {artery_config_name}: {artery_iteration_name}..."
        )
        nuscenes_all_of_iteration = get_nuscenes_all(
            conversion_config=conversion_config,
            artery_config_name=artery_config_name,
            artery_iteration_name=artery_iteration_name,
        )
        nuscenes_all_list.append(nuscenes_all_of_iteration)
        progress.update(iterations_task, advance=1)

    progress.update(configs_task, advance=0.5)

    # Merge the NuScenesAll instances and dump the combined data to the directory
    nuscenes_all_combined = merge_nuscenes_all(nuscenes_all_list)
    dump_to_nuscenes_dir(
        nuscenes_all=nuscenes_all_combined,
        nuscenes_version_dir=conversion_config.get_nuscenes_version_dir(artery_config_name),
        force_overwrite=True,
    )
    progress.update(configs_task, advance=0.5)


def get_structured_artery_log_dirs(eval_config: CustomDataEvalConfig) -> dict[str, list[str]]:
    """returns e.g.
    {
        "artery_config": ["config_iteration_01", "config_iteration_02"],
        "sim01data": ["results_01", "results_02"],
        "sim02data": ["results_01", "results_02"],
    }
    """
    pattern = path.join(eval_config.data_root, eval_config.subdir_pattern, "results_??/")
    matching_dirs = glob.glob(pattern)
    matching_dirs = [dir for dir in matching_dirs if path.isdir(dir)]

    structured_logs: dict[str, list] = {}
    for matching_dir in matching_dirs:
        ns_dir_name = get_nuscenes_dir_name(matching_dir)
        ns_scene_name = get_nuscenes_scene_name(matching_dir)

        if ns_dir_name not in structured_logs:
            structured_logs[ns_dir_name] = []

        structured_logs[ns_dir_name].append(ns_scene_name)

    # Sort dict keys and the lists in their values
    for key, value in structured_logs.items():
        structured_logs[key] = sorted(value)
    structured_logs = {key: structured_logs[key] for key in sorted(structured_logs.keys())}
    return structured_logs


def get_nuscenes_dir_name(artery_log_dir: str) -> str:
    pattern = r"sim\d{2}data"
    matches = re.findall(pattern, artery_log_dir)
    assert len(matches) == 1
    assert isinstance(matches[0], str)
    return matches[0]


def get_nuscenes_scene_name(artery_log_dir: str) -> str:
    pattern = r"results_\d{2}"
    matches = re.findall(pattern, artery_log_dir)
    assert len(matches) == 1
    assert isinstance(matches[0], str)
    return matches[0]


def get_nuscenes_all(
    conversion_config: CustomDataEvalConfig,
    artery_config_name: str,
    artery_iteration_name: str,
) -> NuScenesAll:
    """Converts one artery sim log to a NuScenesAll instance"""
    artery_sim_log = ArterySimLogDump(
        root_dir=path.join(conversion_config.data_root, artery_config_name, artery_iteration_name),
        res_file="localperceptionGT-vehicle_0.out",
        out_file="localperception-vehicle_0.out",
        ego_file="monitor_car-vehicle_0.out",
        map_file="../../sumo_map.png",
    )
    pulled_sim_log: ArterySimLog = pull_artery_sim_log(artery_sim_log_dump=artery_sim_log)

    nuscenes_all: NuScenesAll = convert_to_nuscenes_classes(
        artery_sim_log=pulled_sim_log,
        nuscenes_version_dirname=artery_config_name,
    )
    return nuscenes_all
