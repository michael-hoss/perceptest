import os
import sys
from tempfile import gettempdir

import pytest

from inputs.artery.artery_format import ArteryData, ArterySimLog
from inputs.artery.from_logs.main_loader import pull_artery_data
from inputs.artery.to_nuscenes.to_nuscenes import convert_to_nuscenes_classes, dump_to_nuscenes_dir
from inputs.nuscenes.data_insights import get_reference_track_lenghts, get_submitted_track_lenghts
from inputs.nuscenes.nuscenes_format import NuScenesAll


def test_convert_to_nuscenes(test_case_paths: ArterySimLog) -> None:
    # Preparations: pull artery data into classes from logs
    artery_data: ArteryData = pull_artery_data(artery_sim_log=test_case_paths)

    # Function under test
    nuscenes_version_dirname: str = "artery_to_nuscenes_test"
    nuscenes_all = convert_to_nuscenes_classes(
        artery_data=artery_data, nuscenes_version_dirname=nuscenes_version_dirname
    )

    # Intermediate assertions on the class objects
    assert isinstance(nuscenes_all, NuScenesAll)
    _out_track_lengths: dict = get_submitted_track_lenghts(nuscenes_all=nuscenes_all)
    _res_track_lengths: dict = get_reference_track_lenghts(nuscenes_all=nuscenes_all)

    # Function under test
    nuscenes_dir = os.path.join(gettempdir(), nuscenes_version_dirname)
    dump_to_nuscenes_dir(nuscenes_all=nuscenes_all, nuscenes_version_dir=nuscenes_dir, force_overwrite=True)

    # Assertions on the dumped json files
    # reference data
    assert os.path.exists(os.path.join(nuscenes_dir, "attribute.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "calibrated_sensor.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "ego_pose.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "instance.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "log.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "map.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "category.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "sample.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "sample_annotation.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "sample_data.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "scene.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "sensor.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "visibility.json"))

    # custom data
    assert os.path.exists(os.path.join(nuscenes_dir, "splits.json"))
    assert os.path.exists(os.path.join(nuscenes_dir, "white_map.png"))

    # submission data
    assert os.path.exists(os.path.join(nuscenes_dir, "tracking_results.json"))


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
