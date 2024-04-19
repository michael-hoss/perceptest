import glob
import re
from os import path
from typing import TYPE_CHECKING

from rich.progress import Progress, TaskID  # type: ignore

from inputs.artery.artery_format import ArterySimLog
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes, dump_to_nuscenes_dir
from inputs.nuscenes.nuscenes_format import NuScenesAll
from inputs.nuscenes.nuscenes_format_utils import merge_nuscenes_all

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArteryData

from research.v2x_eval.constants import NUSCENES_DATAROOT


def convert_to_nuscenes_files(
    artery_logs_root_dir: str, nuscenes_version_dirstem: str, force_regenerate: bool = False
) -> None:
    """
    - creates a custom nuscenes dataset version called e.g. "from_artery_v6_simXXdata"
    - makes each individual "results_YY" a separate scene within "from_artery_v6_simXXdata"
    - creates custom splits
        - for each individual results_YY ("results_YY")
        - for all results_YY combined ("all")
    """
    with Progress(refresh_per_second=1) as progress:
        artery_log_dirs: dict = get_structured_artery_log_dirs(artery_logs_root_dir)
        configs_task = progress.add_task("[blue]Converting artery logs to nuScenes...", total=len(artery_log_dirs))
        for artery_config_name, artery_iteration_names in artery_log_dirs.items():
            nuscenes_version_dirname = f"{nuscenes_version_dirstem}_{artery_config_name}"

            # Potentially skip if the nuscenes version directory already exists
            if not force_regenerate and path.exists(path.join(NUSCENES_DATAROOT, nuscenes_version_dirname)):
                progress.update(configs_task, advance=1)
                continue

            convert_artery_config_logs_to_nuscenes_dir(
                artery_logs_root_dir=artery_logs_root_dir,
                progress=progress,
                configs_task=configs_task,
                artery_config_name=artery_config_name,
                artery_iteration_names=artery_iteration_names,
                nuscenes_version_dirname=nuscenes_version_dirname,
            )


def convert_artery_config_logs_to_nuscenes_dir(
    artery_logs_root_dir: str,
    progress: Progress,
    configs_task: TaskID,
    artery_config_name: str,
    artery_iteration_names: list[str],
    nuscenes_version_dirname: str,
):
    iterations_task = progress.add_task("", total=len(artery_iteration_names))
    nuscenes_all_list: list[NuScenesAll] = []

    # Convert each artery config iteration to a NuScenesAll instance
    for artery_iteration_name in artery_iteration_names:
        progress.update(
            iterations_task, description=f"[green]Converting {artery_config_name}: {artery_iteration_name}..."
        )
        nuscenes_all_of_iteration = get_nuscenes_all(
            artery_logs_root_dir=artery_logs_root_dir,
            artery_config_name=artery_config_name,
            artery_iteration_name=artery_iteration_name,
            nuscenes_version_dirname=nuscenes_version_dirname,
        )
        nuscenes_all_list.append(nuscenes_all_of_iteration)
        progress.update(iterations_task, advance=1)

    progress.update(configs_task, advance=0.5)

    # Merge the NuScenesAll instances and dump the combined data to the directory
    nuscenes_all_combined = merge_nuscenes_all(nuscenes_all_list)
    dump_to_nuscenes_dir(
        nuscenes_all=nuscenes_all_combined,
        nuscenes_version_dir=path.join(NUSCENES_DATAROOT, nuscenes_version_dirname),
        force_overwrite=True,
    )
    progress.update(configs_task, advance=0.5)


def get_structured_artery_log_dirs(artery_logs_root_dir: str) -> dict[str, list[str]]:
    """returns e.g.
    {
        "artery_config": ["config_iteration_01", "config_iteration_02"],
        "sim01data": ["results_01", "results_02"],
        "sim02data": ["results_01", "results_02"],
    }
    """
    pattern = path.join(artery_logs_root_dir, "sim??data/results_??/")
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
    artery_logs_root_dir: str, artery_config_name: str, artery_iteration_name: str, nuscenes_version_dirname: str
) -> NuScenesAll:
    """Converts one artery sim log to a NuScenesAll instance"""
    artery_sim_log = ArterySimLog(
        root_dir=path.join(artery_logs_root_dir, artery_config_name, artery_iteration_name),
        res_file="localperceptionGT-vehicle_0.out",
        out_file="localperception-vehicle_0.out",
        ego_file="monitor_car-vehicle_0.out",
    )
    pulled_sim_log: ArteryData = pull_artery_data(artery_sim_log=artery_sim_log)

    nuscenes_all: NuScenesAll = convert_to_nuscenes_classes(
        artery_data=pulled_sim_log,
        nuscenes_version_dirname=nuscenes_version_dirname,
    )
    return nuscenes_all
