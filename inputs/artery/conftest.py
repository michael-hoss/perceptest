import pytest

from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs


def get_test_case_dump() -> ArterySimLogDump:
    """Enable calling this directly for manual tests (anylsis files) that are not pytest tests,
    but rather just bazel py_binary files for easier debugging."""
    dump_v6_sim15_01 = ArterySimLogDump(
        root_dir="/data/sets/KIT_V2X/v6/dataset_last/sim15data/results_01",
        res_file="localperceptionGT-vehicle_0.out",
        out_file="localperception-vehicle_0.out",
        ego_file="monitor_car-vehicle_0.out",
        map_file="../../sumo_map.png",
    )
    return dump_v6_sim15_01


@pytest.fixture
def test_case_dump() -> ArterySimLogDump:
    return get_test_case_dump()


@pytest.fixture
def artery_sim_log(test_case_dump: ArterySimLogDump) -> ArterySimLog:
    return load_from_artery_logs(sim_log_dump=test_case_dump)
