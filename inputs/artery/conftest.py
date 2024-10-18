import os
import shutil

import pytest
import requests  # type: ignore

from base.file_utils.file_utils import compute_file_hash, unzip_file
from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.raw_parsing import load_from_artery_logs


def get_artery_data_root() -> str:
    # Bazel test environment is stripped of all host ENV variables, so we need to
    # specify what we need here. A smoother solution will be appreciated.
    artery_data_root = "/tmp/artery_data_test"
    os.makedirs(artery_data_root, exist_ok=True)
    return artery_data_root


def get_test_cases_zip() -> str:
    data_root = get_artery_data_root()
    zip_file_path = os.path.join(data_root, "artery_data.zip")

    if os.path.isfile(zip_file_path):
        expected_zip_hash = "1b56035be1e4864e0ae678282336318c52c459c83ed56f82ae7861215e4c6662"
        actual_zip_hash = compute_file_hash(file_path=zip_file_path)
        if actual_zip_hash == expected_zip_hash:
            return zip_file_path
        else:
            unzipped_dir = os.path.join(data_root, "example-artery-data")
            os.unlink(zip_file_path)

    shutil.rmtree(unzipped_dir)  # Remove directory and its contents

    artery_url = "https://rwth-aachen.sciebo.de/s/X8WzHWqTwUsEsUz/download"
    response = requests.get(artery_url)
    response.raise_for_status()  # Ensure the request was successful

    with open(zip_file_path, "wb") as f:
        f.write(response.content)
    return zip_file_path


def get_test_cases_dir_from_zip(zip_file_path: str):
    extract_to_dir: str = os.path.dirname(zip_file_path)
    unzipped_dir = os.path.join(extract_to_dir, "example-artery-data")
    if not os.path.isdir(unzipped_dir):
        unzip_file(zip_file_path=zip_file_path, extract_to_dir=extract_to_dir)
    return unzipped_dir


def get_test_case_dump() -> ArterySimLogDump:
    """Enable calling this directly for manual tests (analysis files) that are not pytest tests,
    but rather just bazel py_binary files for easier debugging."""

    zip_file_path: str = get_test_cases_zip()
    unzipped_dir: str = get_test_cases_dir_from_zip(zip_file_path=zip_file_path)

    dump_v6_sim15_01 = ArterySimLogDump(
        root_dir=os.path.join(unzipped_dir, "v6/config_medium/full_run_01"),
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
