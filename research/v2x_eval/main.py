from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs


def convert_and_evaluate() -> dict:
    """Wrap entire data processing for the paper, from the raw Artery logs to the final tables and plots."""

    nuscenes_version_dirstem: str = "from_artery_v6"
    artery_logs_root_dir: str = "/data/sets/KIT_V2X/v6/dataset_last"
    force_regenerate: bool = False  # If False, tries to get existing data from disk for speedup

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
