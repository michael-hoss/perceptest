from nuscenes.eval.tracking.tooling.custom_data_eval_config import CustomDataEvalConfig
from nuscenes.eval.tracking.tooling.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs

from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import convert_to_nuscenes_version_dirs


def convert_and_evaluate(custom_data_eval_config: CustomDataEvalConfig) -> dict:
    convert_to_nuscenes_version_dirs(eval_config=custom_data_eval_config)
    metrics_on_custom_data = obtain_metrics_for_nuscenes_version_dirs(custom_data_eval_config=custom_data_eval_config)
    return metrics_on_custom_data


if __name__ == "__main__":
    use_debugpy()
    config = CustomDataEvalConfig.from_cli()
    convert_and_evaluate(config)
