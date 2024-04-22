from os import path

from inputs.artery.to_nuscenes.to_nuscenes_constants import ArteryConstants
from inputs.nuscenes.nuscenes_format import TrackingSubmission


class ConversionConfig:
    def __init__(self, artery_logs_root_dir: str, force_regenerate: bool) -> None:
        self.artery_logs_root_dir = artery_logs_root_dir
        self.force_regenerate = force_regenerate

        self.nuscenes_eval_config_path = ArteryConstants().nuscenes_eval_config_path
        self.tracking_results_filename = TrackingSubmission.json_filename

        self.metrics_output_dir = "tracking_metrics"  # subdir where metrics are saved to

        self.nuscenes_root_dir = path.join(self.artery_logs_root_dir, "nuscenes")

    def get_tracking_result_path(self, artery_config: str) -> str:
        return path.join(self.nuscenes_root_dir, artery_config, self.tracking_results_filename)

    def get_metrics_output_dir(self, artery_config: str, eval_split: str) -> str:
        return path.join(self.nuscenes_root_dir, artery_config, self.metrics_output_dir, eval_split)

    def get_splits_filename(self, artery_config: str) -> str:
        return path.join(self.nuscenes_root_dir, artery_config, "splits.json")

    def get_nuscenes_version_dir(self, artery_config: str) -> str:
        return path.join(self.nuscenes_root_dir, artery_config)
