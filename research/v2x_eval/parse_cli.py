import argparse

from inputs.artery.to_nuscenes.to_nuscenes_constants import ArteryConstants
from research.v2x_eval.constants import ConversionConfig


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
        help="If flag is set, regenerates all data from scratch",
    )

    parser.add_argument(
        "--nuscenes-eval-config-path",
        type=str,
        help="Path to the config file for the nuscenes tracking evaluation",
        default=ArteryConstants().nuscenes_eval_config_path,
    )

    args = parser.parse_args()
    conversion_config = ConversionConfig(
        custom_data_root=args.artery_logs_root_dir,
        custom_data_subdir_pattern="sim??data",
        force_regenerate=args.force_regenerate,
        nuscenes_eval_config_path=args.nuscenes_eval_config_path,
    )
    return conversion_config
