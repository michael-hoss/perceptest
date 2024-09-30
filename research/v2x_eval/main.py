from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.custom_data_eval_config import CustomDataEvalConfig
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs
from research.v2x_eval.parse_cli import parse_cli


def convert_and_evaluate(custom_data_eval_config: CustomDataEvalConfig) -> dict:
    obtain_nuscenes_version_dirs(eval_config=custom_data_eval_config)
    metrics_on_artery_data = obtain_metrics_for_nuscenes_version_dirs(custom_data_eval_config=custom_data_eval_config)
    return metrics_on_artery_data


if __name__ == "__main__":
    use_debugpy()
    config: CustomDataEvalConfig = parse_cli()
    convert_and_evaluate(config)
