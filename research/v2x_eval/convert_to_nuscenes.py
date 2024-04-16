import glob
import re
from os import path
from typing import TYPE_CHECKING

from tqdm import tqdm  # type: ignore

from inputs.artery.artery_format import ArterySimLog
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes, dump_to_nuscenes_dir
from inputs.nuscenes.nuscenes_format import NuScenesAll
from inputs.nuscenes.nuscenes_format_utils import merge_nuscenes_all

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArteryData

from research.v2x_eval.constants import NUSCENES_DATAROOT


def convert_to_nuscenes_files(artery_logs_root_dir: str, nuscenes_version_dirstem: str) -> None:
    """
    - creates a custom dataset version called e.g. "from_artery_v6_simXXdata"
    - make each individual "results_YY" a separate scene within "from_artery_v6_simXXdata"
    - create splits
    - for each results_YY ("results_YY")
    - for all results_YY ("all")
    """

    artery_log_dirs: dict = get_structured_artery_log_dirs(artery_logs_root_dir)

    for artery_config_name, artery_iteration_names in tqdm(artery_log_dirs.items()):
        nuscenes_all_list: list[NuScenesAll] = []

        nuscenes_version_dirname = f"{nuscenes_version_dirstem}_{artery_config_name}"

        for artery_iteration_name in artery_iteration_names:
            artery_sim_log = ArterySimLog(
                root_dir=path.join(artery_logs_root_dir, artery_config_name, artery_iteration_name),
                res_file="localperceptionGT-vehicle_0.out",
                out_file="localperception-vehicle_0.out",
                ego_file="monitor_car-vehicle_0.out",
            )
            pulled_sim_log: ArteryData = pull_artery_data(artery_sim_log=artery_sim_log)

            nuscenes_all_of_artery_iteration: NuScenesAll = convert_to_nuscenes_classes(
                artery_data=pulled_sim_log,
                nuscenes_version_dirname=nuscenes_version_dirname,
            )
            nuscenes_all_list.append(nuscenes_all_of_artery_iteration)

        nuscenes_all_combined = merge_nuscenes_all(nuscenes_all_list)

        nuscenes_dump_dir: str = path.join(NUSCENES_DATAROOT, nuscenes_version_dirname)
        dump_to_nuscenes_dir(
            nuscenes_all=nuscenes_all_combined, nuscenes_version_dir=nuscenes_dump_dir, force_overwrite=True
        )


def get_structured_artery_log_dirs(artery_logs_root_dir: str) -> dict[str, list]:
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
