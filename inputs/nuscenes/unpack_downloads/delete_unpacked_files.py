import os


def delete_already_unpacked_archives(file_list_path: str):
    try:
        with open(file_list_path, "r") as file:
            file_paths = file.read().splitlines()
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_list_path}")


if __name__ == "__main__":
    download_dir = os.path.expanduser("~/Downloads/")
    unpacked_files_list = os.path.join(download_dir, "already_unpacked_files.txt")

    delete_already_unpacked_archives(file_list_path=unpacked_files_list)
