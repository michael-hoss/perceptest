import sys

import pytest

from conftest import use_debugpy
from inputs.artery.artery_format import ArteryData, FilePaths
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import tidy_up_timestamps


def test_load_example_log_files_pass(test_case_paths: FilePaths) -> None:
    """This tests the code for loading the artery logs."""

    # Function under test
    artery_data = load_from_artery_logs(file_paths=test_case_paths)

    # Assertions
    assert isinstance(artery_data, ArteryData)


def test_map_to_common_time_stamps_pass(artery_data: ArteryData) -> None:
    # Function under test
    # After v5, the timestamps are already aligned.
    # However, there might still be overhanging time stamps that need to be removed.
    tidy_up_timestamps(artery_data=artery_data)

    # Trivial assertions
    assert isinstance(artery_data, ArteryData)
    assert len(artery_data.timestamps) > 0

    # Assert that the common beginning and end stamps are present in OuT, ReS, and ego data
    assert artery_data.timestamps[0] == min(
        [out_traj[0]["origin"]["timestamp"] for out_traj in artery_data.objects_out.values()]
    )
    assert artery_data.timestamps[-1] == max(
        [out_traj[-1]["origin"]["timestamp"] for out_traj in artery_data.objects_out.values()]
    )
    assert artery_data.timestamps[0] == min(
        [res_traj[0]["origin"]["timestamp"] for res_traj in artery_data.objects_res.values()]
    )
    assert artery_data.timestamps[-1] == max(
        [res_traj[-1]["origin"]["timestamp"] for res_traj in artery_data.objects_res.values()]
    )
    assert artery_data.timestamps[0] == artery_data.ego_vehicle[0]["origin"]["timestamp"]
    assert artery_data.timestamps[-1] == artery_data.ego_vehicle[-1]["origin"]["timestamp"]


if __name__ == "__main__":
    args = sys.argv[1:]
    use_debugpy()
    sys.exit(pytest.main([__file__, "-vv"] + args))
