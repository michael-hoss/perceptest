from os import path
from typing import TYPE_CHECKING

from conftest import use_debugpy
from inputs.artery.artery_format import FilePaths
from inputs.artery.conftest import get_test_case_paths
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes, dump_to_nuscenes_dir
from inputs.artery.to_nuscenes.to_nuscenes_constants import ArteryConstants
from inputs.nuscenes.evaluate_tracking import (
    TrackingConfig,
    get_nuscenes_tracking_config_from_own_file,
    nuscenes_devkit_tracking_eval,
)
from inputs.nuscenes.nuscenes_format import TrackingEvalParams

if TYPE_CHECKING:
    from inputs.artery.artery_format import ArteryData


ARTERY_RAW_PATHS: FilePaths = get_test_case_paths()
NUSCENES_EVAL_CONFIG_PATH = ArteryConstants().nuscenes_eval_config_path
NUSCENES_DATAROOT = "/data/sets/nuscenes"
NUSCENES_VERSION_DIRNAME = "from_artery_v6_sim15_01"


"""Notes:

Options for organizing different simulation runs in artery:
- dataset version dirs
- splits in that dir
- scenes in one or multiple splits.

The tracking eval command then takes a version and a split as input and computes the metrics for all
scens in that split.

TODO:
- create a custom dataset version called e.g. "from_artery_v5"
- make each individual simXXdata/results_YY a separate scene
- create splits
  - for each individual scene
  - for all scenes of a simXXdata
  - for all scenes
"""


def eval_artery_on_nuscenes() -> None:
    artery_data: ArteryData = pull_artery_data(file_paths=ARTERY_RAW_PATHS)
    nuscenes_all = convert_to_nuscenes_classes(
        artery_data=artery_data, nuscenes_version_dirname=NUSCENES_VERSION_DIRNAME
    )

    nuscenes_dump_dir = path.join(NUSCENES_DATAROOT, NUSCENES_VERSION_DIRNAME)
    dump_to_nuscenes_dir(nuscenes_all=nuscenes_all, nuscenes_version_dir=nuscenes_dump_dir, force_overwrite=True)

    tracking_eval_params = TrackingEvalParams(
        result_path=path.join(nuscenes_dump_dir, "tracking_results.json"),
        output_dir=path.join(nuscenes_dump_dir, "tracking_evalution_metrics"),
        eval_set="all",  # see python-sdk/nuscenes/utils/splits.py
        nusc_dataroot=NUSCENES_DATAROOT,
        nusc_version=NUSCENES_VERSION_DIRNAME,
    )

    config: TrackingConfig = get_nuscenes_tracking_config_from_own_file(config_path=NUSCENES_EVAL_CONFIG_PATH)
    _metrics_summary = nuscenes_devkit_tracking_eval(params=tracking_eval_params, config=config)
    pass


if __name__ == "__main__":
    use_debugpy()
    eval_artery_on_nuscenes()
