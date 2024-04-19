import argparse

from conftest import use_debugpy
from research.v2x_eval.convert_to_nuscenes import obtain_nuscenes_version_dirs
from research.v2x_eval.obtain_tracking_metrics import obtain_metrics_for_nuscenes_version_dirs


def convert_and_evaluate(cli_args) -> dict:
    obtain_nuscenes_version_dirs(
        artery_logs_root_dir=cli_args.artery_logs_root_dir,
        nuscenes_version_dirstem=cli_args.nuscenes_version_dirstem,
        force_regenerate=cli_args.force_regenerate,
    )
    metrics_of_configs = obtain_metrics_for_nuscenes_version_dirs(
        artery_logs_root_dir=cli_args.artery_logs_root_dir,
        nuscenes_version_dirstem=cli_args.nuscenes_version_dirstem,
        force_regenerate=cli_args.force_regenerate,
    )
    return metrics_of_configs


def parse_cli():
    parser = argparse.ArgumentParser(
        description="Wrap entire data processing for the paper, from the raw artery logs to the final tables and plots."
    )

    parser.add_argument(
        "--nuscenes_version_dirstem",
        type=str,
        help="Prefix of the nuscenes version dir to which the artery data will be converted",
        default="from_artery_v6",
    )
    parser.add_argument(
        "--artery_logs_root_dir",
        type=str,
        help="Root directory of the artery logs (input data)",
        default="/data/sets/KIT_V2X/v6/dataset_last",
    )
    parser.add_argument(
        "--force_regenerate",
        action="store_true",
        default=False,
        help="If True, regenerates all data from scratch",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    use_debugpy()
    cli_args = parse_cli()
    convert_and_evaluate(cli_args)
