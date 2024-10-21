from nuscenes.eval.tracking.tooling.custom_data_eval_config import CustomDataEvalConfig
from nuscenes.eval.tracking.tooling.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs

from conftest import use_debugpy
from inputs.artery.obtain_test_data import obtain_test_cases
from research.v2x_eval.convert_to_nuscenes import convert_to_nuscenes_version_dirs


def convert_and_evaluate(custom_data_eval_config: CustomDataEvalConfig) -> dict:
    convert_to_nuscenes_version_dirs(eval_config=custom_data_eval_config)
    metrics_on_custom_data: dict = obtain_metrics_for_nuscenes_version_dirs(
        custom_data_eval_config=custom_data_eval_config
    )
    return metrics_on_custom_data


if __name__ == "__main__":
    use_debugpy()

    example_data_dir: str = obtain_test_cases()

    config = CustomDataEvalConfig(
        data_root=example_data_dir,
        force_regenerate=True,
        subdir_pattern="sim??data",
        nuscenes_eval_config_path="inputs/artery/to_nuscenes/artery_config_for_nuscenes.json",
    )
    convert_and_evaluate(config)
