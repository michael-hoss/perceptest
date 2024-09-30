from os import path

from nuscenes.eval.tracking.tooling.nuscenes_format import TrackingSubmission


class CustomDataEvalConfig:
    def __init__(
        self,
        data_root: str,
        subdir_pattern: str,
        force_regenerate: bool,
        nuscenes_eval_config_path: str,
    ) -> None:
        """Config for
        1) conversion of custom data to nuScenes tracking format on disc
        2) subsequent evaluation of nuscenes tracking metrics on those converted data.

        This class assumes that the actual custom data is stored in subdirs named subdir_pattern.
        For each of these subdirs, the converter should create a separate nuscenes-compliant subdir.
        """

        # Root dir of custom data
        self.data_root = data_root

        # Pattern for subdirectories of original data, which will be converted to separate nuScenes dirs.
        # These subdirs will act as different nuscenes dataset versions (as e.g. `v1.0-mini` in the original)
        self.subdir_pattern = subdir_pattern

        # Force the re-generation of converted data or tracking metrics, rather than reading cached results from disc.
        # This flag is used by the metrics computation, and can also be implemented by a custom converter.
        self.force_regenerate = force_regenerate

        # Path to JSON config for tracking evaluation, as expected by nuscenes-devkit
        self.nuscenes_eval_config_path = nuscenes_eval_config_path

        # Convention for naming of data under test
        self.tracking_results_filename = TrackingSubmission.json_filename

        # Store nuScenes data below original data in a subdir
        self.nuscenes_format_root_dir = path.join(self.data_root, "nuscenes")

        # Subdir where tracking metrics output files will be saved to
        self.metrics_output_dir = "tracking_metrics"

    def get_tracking_result_path(self, data_config: str) -> str:
        return path.join(self.nuscenes_format_root_dir, data_config, self.tracking_results_filename)

    def get_metrics_output_dir(self, data_config: str, eval_split: str) -> str:
        return path.join(self.nuscenes_format_root_dir, data_config, self.metrics_output_dir, eval_split)

    def get_splits_filename(self, data_config: str) -> str:
        return path.join(self.nuscenes_format_root_dir, data_config, "splits.json")

    def get_nuscenes_version_dir(self, data_config: str) -> str:
        return path.join(self.nuscenes_format_root_dir, data_config)
