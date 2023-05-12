import pytest

from inputs.artery.artery_format import ArteryData, FilePaths
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs


def get_test_case_paths() -> FilePaths:
    """Enable calling this directly for manual tests (anylsis files) that are not pytest tests,
    but rather just bazel py_binary files for easier debugging."""
    paths_v6_sim15_01 = FilePaths(
        root_dir="/data/sets/KIT_V2X/v6/dataset_last/sim15data/results_01",
        res_file="localperceptionGT-vehicle_0.out",
        out_file="localperception-vehicle_0.out",
        ego_file="monitor_car-vehicle_0.out",
    )
    return paths_v6_sim15_01


@pytest.fixture
def test_case_paths() -> FilePaths:
    return get_test_case_paths()


@pytest.fixture
def artery_data(test_case_paths: FilePaths) -> ArteryData:
    return load_from_artery_logs(file_paths=test_case_paths)
