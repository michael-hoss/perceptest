import glob
import re
from os import path
from typing import TYPE_CHECKING

from inputs.artery.artery_format import ArterySimLog
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes, dump_to_nuscenes_dir

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArteryData

from research.v2x_eval.constants import NUSCENES_DATAROOT

"""Notes:

Options for organizing different simulation runs in artery:
- dataset version dirs
- splits in that dir
- scenes in one or multiple splits.

The tracking eval command then takes a version and a split as input and computes the metrics for all
scens in that split.

TODO:
- create a custom dataset version called e.g. "from_artery_v6_simXXdata"
- make each individual "results_YY" a separate scene within "from_artery_v6_simXXdata"
- create splits
  - for each results_YY ("results_YY")
  - for all results_YY ("all")
"""


def convert_to_nuscenes_files(artery_logs_root_dir: str, nuscenes_version_dirname: str) -> None:
    artery_log_dirs: dict = get_structured_artery_log_dirs(artery_logs_root_dir)

    for artery_config_name, artery_iteration_names in artery_log_dirs.items():
        pulled_iterations: list[ArteryData] = []

        for artery_iteration_name in artery_iteration_names:
            artery_sim_log = ArterySimLog(
                root_dir=path.join(artery_logs_root_dir, artery_config_name, artery_iteration_name),
                res_file="localperceptionGT-vehicle_0.out",
                out_file="localperception-vehicle_0.out",
                ego_file="monitor_car-vehicle_0.out",
            )
            pulled_iterations.append(pull_artery_data(artery_sim_log=artery_sim_log))

        # TODO convert multiple artery log directories into the same nuscenes directory!

        nuscenes_all = convert_to_nuscenes_classes(
            artery_data=pulled_iterations[0],  # TODO enable this for list[ArteryData]
            nuscenes_version_dirname=nuscenes_version_dirname,
        )

        nuscenes_dump_dir: str = path.join(NUSCENES_DATAROOT, nuscenes_version_dirname)
        dump_to_nuscenes_dir(nuscenes_all=nuscenes_all, nuscenes_version_dir=nuscenes_dump_dir, force_overwrite=True)


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
