from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import convert_to_nuscenes_files


def convert_and_evaluate() -> None:
    nuscenes_version_dirstem: str = "from_artery_v6"
    artery_logs_root_dir: str = "/data/sets/KIT_V2X/v6/dataset_last"
    force_regenerate: bool = False

    convert_to_nuscenes_files(
        artery_logs_root_dir=artery_logs_root_dir,
        nuscenes_version_dirstem=nuscenes_version_dirstem,
        force_regenerate=force_regenerate,
    )
    # compute_metrics_for_all_splits() # TODO


if __name__ == "__main__":
    use_debugpy()
    convert_and_evaluate()
