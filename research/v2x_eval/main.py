import argparse

from conftest import use_debugpy
from research.v2x_eval.constants import ConversionConfig
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs


def convert_and_evaluate(conversion_config: ConversionConfig) -> dict:
    obtain_nuscenes_version_dirs(conversion_config=conversion_config)
    metrics_on_artery_data = obtain_metrics_for_nuscenes_version_dirs(conversion_config=conversion_config)
    return metrics_on_artery_data


def parse_cli() -> ConversionConfig:
    parser = argparse.ArgumentParser(
        description="Wrap entire data processing for the paper, from the raw artery logs to the final tables and plots."
    )

    parser.add_argument(
        "--artery-logs-root-dir",
        type=str,
        help="Root directory of the artery logs (input data)",
        default="/data/sets/KIT_V2X/v6/dataset_last",
    )
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        default=False,
        help="If True, regenerates all data from scratch",
    )

    args = parser.parse_args()
    conversion_config = ConversionConfig(
        artery_logs_root_dir=args.artery_logs_root_dir, force_regenerate=args.force_regenerate
    )
    return conversion_config


if __name__ == "__main__":
    use_debugpy()
    config: ConversionConfig = parse_cli()
    convert_and_evaluate(config)
