import os

import pytest
import requests  # type: ignore

from base.file_utils.file_utils import compute_file_hash, silent_remove_dir, silent_remove_file, unzip_file
from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs

# Keep those up-to-date!
TEST_ZIP_DOWNLOAD_URL = "https://rwth-aachen.sciebo.de/s/X8WzHWqTwUsEsUz/download"
TEST_ZIP_HASH = "141eaef417ea1843bfafb30218c17e82a35d79f077051283d529550a5c3a27f9"


def get_artery_data_root() -> str:
    # Bazel test environment is stripped of all host ENV variables, so we need to
    # specify what we need here. A smoother solution will be appreciated.
    artery_data_root = "/tmp/artery_data_test"
    os.makedirs(artery_data_root, exist_ok=True)
    return artery_data_root


def get_test_cases_zip(zip_file_path: str, unzipped_dir: str) -> None:
    if not correct_zip_file_exists(zip_file_path=zip_file_path):
        silent_remove_file(file=zip_file_path)
        silent_remove_dir(dir=unzipped_dir)
        download_zip_file(zip_file_path=zip_file_path)


def correct_zip_file_exists(zip_file_path: str) -> bool:
    if os.path.isfile(zip_file_path):
        actual_zip_hash = compute_file_hash(file_path=zip_file_path)
        if actual_zip_hash == TEST_ZIP_HASH:
            return True
    return False


def download_zip_file(zip_file_path: str) -> None:
    response = requests.get(TEST_ZIP_DOWNLOAD_URL)
    response.raise_for_status()  # Ensure the request was successful

    with open(zip_file_path, "wb") as f:
        f.write(response.content)

    assert compute_file_hash(file_path=zip_file_path) == TEST_ZIP_HASH


def get_test_cases_dir_from_zip(zip_file_path: str, unzipped_dir: str) -> None:
    extract_to_dir: str = os.path.dirname(unzipped_dir)
    if not os.path.isdir(unzipped_dir):
        unzip_file(zip_file_path=zip_file_path, extract_to_dir=extract_to_dir)
    else:
        # We assume the data is already correctly unzipped froma previous execution
        pass


def get_test_case_dump() -> ArterySimLogDump:
    """Enable calling this directly for manual tests (analysis files) that are not pytest tests,
    but rather just bazel py_binary files for easier debugging."""

    data_root = get_artery_data_root()
    zip_file_path = os.path.join(data_root, "artery_data.zip")
    unzipped_dir = os.path.join(data_root, "example-artery-data")

    get_test_cases_zip(zip_file_path=zip_file_path, unzipped_dir=unzipped_dir)
    get_test_cases_dir_from_zip(zip_file_path=zip_file_path, unzipped_dir=unzipped_dir)

    dump_v6_sim15_01 = ArterySimLogDump(
        root_dir=os.path.join(unzipped_dir, "v6/sim15data/results_01"),
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
