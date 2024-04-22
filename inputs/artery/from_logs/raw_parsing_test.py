import sys

import pytest

from conftest import use_debugpy
from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs
from inputs.artery.from_logs.timestamps import tidy_up_timestamps


def test_load_example_log_files_pass(test_case_dump: ArterySimLogDump) -> None:
    """This tests the code for loading the artery logs."""

    # Function under test
    artery_sim_log = load_from_artery_logs(sim_log_dump=test_case_dump)

    # Assertions
    assert isinstance(artery_sim_log, ArterySimLog)


def test_map_to_common_time_stamps_pass(artery_sim_log: ArterySimLog) -> None:
    # Function under test
    # After v5, the timestamps are already aligned.
    # However, there might still be overhanging time stamps that need to be removed.
    tidy_up_timestamps(artery_sim_log=artery_sim_log)

    # Trivial assertions
    assert isinstance(artery_sim_log, ArterySimLog)
    assert len(artery_sim_log.timestamps) > 0

    # Assert that the common beginning and end stamps are present in OuT, ReS, and ego data
    assert artery_sim_log.timestamps[0] == min(
        [out_traj[0]["origin"]["timestamp"] for out_traj in artery_sim_log.objects_out.values()]
    )
    assert artery_sim_log.timestamps[-1] == max(
        [out_traj[-1]["origin"]["timestamp"] for out_traj in artery_sim_log.objects_out.values()]
    )
    assert artery_sim_log.timestamps[0] == min(
        [res_traj[0]["origin"]["timestamp"] for res_traj in artery_sim_log.objects_res.values()]
    )
    assert artery_sim_log.timestamps[-1] == max(
        [res_traj[-1]["origin"]["timestamp"] for res_traj in artery_sim_log.objects_res.values()]
    )
    assert artery_sim_log.timestamps[0] == artery_sim_log.ego_vehicle[0]["origin"]["timestamp"]
    assert artery_sim_log.timestamps[-1] == artery_sim_log.ego_vehicle[-1]["origin"]["timestamp"]


if __name__ == "__main__":
    args = sys.argv[1:]
    use_debugpy()
    sys.exit(pytest.main([__file__, "-vv"] + args))
