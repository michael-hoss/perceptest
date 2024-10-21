import contextlib
import hashlib
import os
import shutil
import time
import zipfile


def compute_file_hash(file_path, hash_algo="sha256"):
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def unzip_file(zip_file_path: str, extract_to_dir: str):
    if zipfile.is_zipfile(zip_file_path):
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to_dir)
    else:
        raise Exception(f"{zip_file_path} is not a valid zip file")


def silent_remove_file(file: str) -> None:
    try:
        os.unlink(file)
    except FileNotFoundError:
        pass


def silent_remove_dir(dir: str) -> None:
    try:
        shutil.rmtree(dir)  # Remove directory and its contents
    except FileNotFoundError:
        pass


def create_lock_file(lock_file: str) -> None:
    with open(lock_file, "w") as f:
        f.write("This file indicates a process is running.")
    print(f"Lock file {lock_file} created.")


def delete_lock_file(lock_file: str) -> None:
    if os.path.exists(lock_file):
        os.remove(lock_file)
        print(f"Lock file {lock_file} deleted.")
    else:
        print(f"Lock file {lock_file} not found.")


def wait_until_existing_lock_file_gone(lock_file: str, timeout: float = 20.0) -> None:
    """timeout is in secs"""

    start_time = time.time()
    while os.path.isfile(lock_file):
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise RuntimeError(f"Lock file existed longer than {timeout}s")

        print(f"Waiting for lock file to disappear: {elapsed_time:.2f}s of {timeout:.2f}s")
        time.sleep(timeout / 10.0)


@contextlib.contextmanager
def lock_file_manager(lock_file):
    wait_until_existing_lock_file_gone(lock_file=lock_file)

    try:
        create_lock_file(lock_file=lock_file)
        yield  # Allow code within 'with' block to execute
    finally:
        delete_lock_file(lock_file=lock_file)
