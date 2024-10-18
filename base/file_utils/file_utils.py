import hashlib
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
