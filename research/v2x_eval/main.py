from conftest import use_debugpy
from research.v2x_eval.constants import ConversionConfig
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs
from research.v2x_eval.parse_cli import parse_cli


def convert_and_evaluate(conversion_config: ConversionConfig) -> dict:
    obtain_nuscenes_version_dirs(conversion_config=conversion_config)
    metrics_on_artery_data = obtain_metrics_for_nuscenes_version_dirs(conversion_config=conversion_config)
    return metrics_on_artery_data


if __name__ == "__main__":
    use_debugpy()
    config: ConversionConfig = parse_cli()
    convert_and_evaluate(config)
