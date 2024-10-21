import math
import os
import sys

import pytest
from nuscenes.eval.tracking.tooling.custom_data_eval_config import CustomDataEvalConfig

from inputs.artery.obtain_test_data import obtain_test_cases
from research.v2x_eval.main import convert_and_evaluate


def test_main_pass() -> None:
    # Prepare test data and config
    example_data_dir: str = obtain_test_cases()

    config = CustomDataEvalConfig(
        data_root=example_data_dir,
        force_regenerate=True,
        subdir_pattern="sim15data",
        nuscenes_eval_config_path="inputs/artery/to_nuscenes/artery_config_for_nuscenes.json",
    )

    # Function under test
    metrics_on_example_data = convert_and_evaluate(config)

    # Assertions
    assert isinstance(metrics_on_example_data, dict)
    metrics_output_dir = os.path.join(example_data_dir, "nuscenes/sim15data/tracking_metrics")
    assert os.path.isdir(os.path.join(metrics_output_dir, "all"))
    assert os.path.isdir(os.path.join(metrics_output_dir, "results_01"))
    assert os.path.isdir(os.path.join(metrics_output_dir, "results_02"))
    assert math.isclose(metrics_on_example_data["sim15data"]["results_01"]["amota"], 0.6900355871886121)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
