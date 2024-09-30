from os import path

from nuscenes.eval.tracking.tooling.nuscenes_format import TrackingSubmission


class ConversionConfig:
    def __init__(
        self,
        custom_data_root: str,
        custom_data_subdir_pattern: str,
        force_regenerate: bool,
        nuscenes_eval_config_path: str,
    ) -> None:
        """Config for conversion of custom data to nuScenes tracking format on disc, and subsequent
        evaluation of tracking metrics on the converted data."""

        # Root dir of custom data
        self.custom_data_root = custom_data_root

        # pattern for subdirectories of original logs, which will be converted to separate nuScenes dirs
        self.custom_data_subdir_pattern = custom_data_subdir_pattern

        # for the re-generation of converted data or tracking metrics, rather than taking cached results
        self.force_regenerate = force_regenerate

        # Path to JSON config for tracking evaluation
        self.nuscenes_eval_config_path = nuscenes_eval_config_path

        self.tracking_results_filename = TrackingSubmission.json_filename

        self.metrics_output_dir = "tracking_metrics"  # subdir where metrics are saved to

        # Store nuScenes data below original data in a subdir
        self.nuscenes_root_dir = path.join(self.custom_data_root, "nuscenes")

    def get_tracking_result_path(self, data_config: str) -> str:
        return path.join(self.nuscenes_root_dir, data_config, self.tracking_results_filename)

    def get_metrics_output_dir(self, data_config: str, eval_split: str) -> str:
        return path.join(self.nuscenes_root_dir, data_config, self.metrics_output_dir, eval_split)

    def get_splits_filename(self, data_config: str) -> str:
        return path.join(self.nuscenes_root_dir, data_config, "splits.json")

    def get_nuscenes_version_dir(self, data_config: str) -> str:
        return path.join(self.nuscenes_root_dir, data_config)
