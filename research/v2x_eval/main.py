from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs


def convert_and_evaluate() -> dict:
    """Wrap entire data processing for the paper, from the raw artery logs to the final tables and plots."""

    # Prefix of the nuscenes version dir to which the artery data is converted
    nuscenes_version_dirstem: str = "from_artery_v6"

    # The input data from artery is expected here
    artery_logs_root_dir: str = "/data/sets/KIT_V2X/v6/dataset_last"

    # If False, tries to read previously computed data from disk to speed up recomputations
    force_regenerate: bool = False

    obtain_nuscenes_version_dirs(
        artery_logs_root_dir=artery_logs_root_dir,
        nuscenes_version_dirstem=nuscenes_version_dirstem,
        force_regenerate=force_regenerate,
    )
    metrics_of_configs = obtain_metrics_for_nuscenes_version_dirs(
        nuscenes_version_dirstem=nuscenes_version_dirstem, force_regenerate=force_regenerate
    )
    return metrics_of_configs


if __name__ == "__main__":
    use_debugpy()
    convert_and_evaluate()
