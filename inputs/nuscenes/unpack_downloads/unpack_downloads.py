import os
import re
import tarfile

from delete_unpacked_files import delete_already_unpacked_archives  # type: ignore


def create_file_if_not_exists(file_path: str) -> None:
    try:
        # 'x' mode creates the file, but raises an error if it already exists
        with open(file_path, "x"):
            pass
        print(f"File created: {file_path}")
    except FileExistsError:
        pass


def is_file_in_list(file_path_to_check: str, file_list_path: str) -> bool:
    with open(file_list_path, "r") as file:
        file_paths = file.read().splitlines()
        return file_path_to_check in file_paths


def append_to_file_list(file_list_path: str, new_file_path: str) -> None:
    with open(file_list_path, "a") as file:
        file.write(new_file_path + "\n")


def get_matching_file_paths(directory: str, pattern: str) -> list[str]:
    file_paths = []

    # Iterate through files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if the file path matches the pattern
        if re.match(pattern, file_name):
            file_paths.append(file_path)

    return file_paths


def unpack_files(source_dir: str, file_pattern: str, destination_dir: str, unpacked_files_list: str):
    print("-> Unpacking files <-")
    print(f"Source dir: {source_dir}")
    print(f"Desitnation dir: {destination_dir}")
    print(f"File pattern: {file_pattern}")
    print(f"Using this list to keep track of what has been unpacked already: {unpacked_files_list}")

    matching_files: list[str] = get_matching_file_paths(directory=source_dir, pattern=file_pattern)
    matching_files.sort()

    for file_path in matching_files:
        # Make space already now because of limited disk space
        delete_already_unpacked_archives(file_list_path=unpacked_files_list)

        unpacked_previously: bool = is_file_in_list(file_path, unpacked_files_list)
        if unpacked_previously:
            print(f"Skipping {os.path.basename(file_path)}, already unpacked.")
            continue

        # Unpack the file
        with tarfile.open(file_path, "r") as tar:
            print(f"Unpacking {os.path.basename(file_path)} ...", end="")
            tar.extractall(path=destination_dir)
            print(" Done.", end="")

        # Remember it has been unpacked
        append_to_file_list(file_list_path=unpacked_files_list, new_file_path=file_path)
        print(" Unpacking registered.")


if __name__ == "__main__":
    # Parameters
    download_dir = os.path.expanduser("~/Downloads/")
    file_pattern = r"v1\.0-(trainval|test).*\.(tgz|tar)"
    # destination_dir = os.path.join(download_dir, "nuscenes_playground")
    destination_dir = os.environ.get("NUSCENES", "/data/sets/nuscenes")
    unpacked_files_list = os.path.join(download_dir, "already_unpacked_files.txt")

    create_file_if_not_exists(unpacked_files_list)
    unpack_files(
        source_dir=download_dir,
        file_pattern=file_pattern,
        destination_dir=destination_dir,
        unpacked_files_list=unpacked_files_list,
    )
