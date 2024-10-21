import os
import time

import requests  # type: ignore

from base.file_utils.file_utils import (
    compute_file_hash,
    silent_remove_dir,
    silent_remove_file,
    unzip_file,
)
from base.file_utils.lock_file import lock_file_manager

# Keep those up-to-date!
TEST_ZIP_DOWNLOAD_URL = "https://rwth-aachen.sciebo.de/s/X8WzHWqTwUsEsUz/download"
EXPECTED_TEST_ZIP_HASH = "141eaef417ea1843bfafb30218c17e82a35d79f077051283d529550a5c3a27f9"


def get_artery_data_root() -> str:
    artery_data_root = os.environ.get("ARTERY_DATA_ROOT")
    if not artery_data_root:
        raise Exception("Need to specify ARTERY_DATA_ROOT")

    os.makedirs(artery_data_root, exist_ok=True)
    return artery_data_root


def obtain_test_cases_zip(zip_file_path: str, unzipped_dir: str) -> None:
    if not correct_zip_file_exists(zip_file_path=zip_file_path):
        silent_remove_file(file=zip_file_path)
        silent_remove_dir(dir=unzipped_dir)
        download_zip_file(zip_file_path=zip_file_path)


def correct_zip_file_exists(zip_file_path: str) -> bool:
    if os.path.isfile(zip_file_path):
        actual_zip_hash = compute_file_hash(file_path=zip_file_path)
        print("Found artery test data with hash", actual_zip_hash)
        if actual_zip_hash == EXPECTED_TEST_ZIP_HASH:
            print("Skipping download: local hash matches expected hash")
            return True
    return False


def download_zip_file(zip_file_path: str) -> None:
    print("Starting download of zip file from", TEST_ZIP_DOWNLOAD_URL)
    start_time = time.time()
    response = requests.get(TEST_ZIP_DOWNLOAD_URL)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Download time: {duration:.2f} seconds")
    response.raise_for_status()  # Ensure the request was successful

    with open(zip_file_path, "wb") as f:
        f.write(response.content)

    downloaded_zip_hash: str = compute_file_hash(file_path=zip_file_path)
    print("Downloaded zip with hash", downloaded_zip_hash)
    assert downloaded_zip_hash == EXPECTED_TEST_ZIP_HASH
    print("Hash matches expected hash.")


def obtain_test_cases_dir_from_zip(zip_file_path: str, unzipped_dir: str) -> None:
    extract_to_dir: str = os.path.dirname(unzipped_dir)
    if not os.path.isdir(unzipped_dir):
        unzip_file(zip_file_path=zip_file_path, extract_to_dir=extract_to_dir)
        print("Unzipped contents of ", zip_file_path, "to", extract_to_dir)
    else:
        print("Skippig the unzip: dir already present")


def obtain_test_cases() -> str:
    data_root = get_artery_data_root()
    zip_file_path = os.path.join(data_root, "artery_data.zip")
    unzipped_dir = os.path.join(data_root, "example-artery-data")

    with lock_file_manager(lock_file=os.path.join(data_root, "download_in_progress.lock")):
        obtain_test_cases_zip(zip_file_path=zip_file_path, unzipped_dir=unzipped_dir)
        obtain_test_cases_dir_from_zip(zip_file_path=zip_file_path, unzipped_dir=unzipped_dir)

    return unzipped_dir


if __name__ == "__main__":
    obtain_test_cases()
