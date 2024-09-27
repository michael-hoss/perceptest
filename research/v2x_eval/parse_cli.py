import argparse

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

    args = parser.parse_args()
    conversion_config = ConversionConfig(
        artery_logs_root_dir=args.artery_logs_root_dir, force_regenerate=args.force_regenerate
    )
    return conversion_config
