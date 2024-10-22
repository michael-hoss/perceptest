import os
import sys

import pytest
from nuscenes.eval.tracking.tooling.custom_data_eval_config import CustomDataEvalConfig

from base.testing.recursive_assert_equal import SKIP_TEST_HINT, assert_equal
from inputs.artery.obtain_test_data import obtain_test_cases
from research.v2x_eval.main import convert_and_evaluate


def get_expected_metrics_on_example_data() -> dict:
    return {
        "sim15data": {
            "results_01": {
                "label_metrics": {
                    "amota": {"car": 0.6900355871886121},
                    "amotp": {"car": 1.0140107170360877},
                    "recall": {"car": 0.9195106245975532},
                    "motar": {"car": 0.7886120996441282},
                    "gt": {"car": 1553.0},
                    "mota": {"car": 0.713457823567289},
                    "motp": {"car": 0.8731551051841},
                    "mt": {"car": 14.0},
                    "ml": {"car": 1.0},
                    "faf": {"car": 282.8571428571429},
                    "tp": {"car": 1405.0},
                    "fp": {"car": 297.0},
                    "fn": {"car": 125.0},
                    "ids": {"car": 23.0},
                    "frag": {"car": 8.0},
                    "tid": {"car": 0.07142857142857142},
                    "lgd": {"car": 0.5714285714285714},
                },
                "eval_time": SKIP_TEST_HINT,
                "cfg": {
                    "tracking_names": ["car"],
                    "pretty_tracking_names": {"car": "Car"},
                    "tracking_colors": {"car": "C0"},
                    "class_range": {"car": 1000000.0},
                    "dist_fcn": "center_distance",
                    "dist_th_tp": 2.0,
                    "min_recall": 0.1,
                    "max_boxes_per_sample": 500,
                    "metric_worst": {
                        "amota": 0.0,
                        "amotp": 2.0,
                        "recall": 0.0,
                        "motar": 0.0,
                        "mota": 0.0,
                        "motp": 2.0,
                        "mt": 0.0,
                        "ml": -1.0,
                        "faf": 500,
                        "gt": -1,
                        "tp": 0.0,
                        "fp": -1.0,
                        "fn": -1.0,
                        "ids": -1.0,
                        "frag": -1.0,
                        "tid": 20,
                        "lgd": 20,
                    },
                    "num_thresholds": 40,
                },
                "amota": 0.6900355871886121,
                "amotp": 1.0140107170360877,
                "recall": 0.9195106245975532,
                "motar": 0.7886120996441282,
                "gt": 1553.0,
                "mota": 0.713457823567289,
                "motp": 0.8731551051841,
                "mt": 14.0,
                "ml": 1.0,
                "faf": 282.8571428571429,
                "tp": 1405.0,
                "fp": 297.0,
                "fn": 125.0,
                "ids": 23.0,
                "frag": 8.0,
                "tid": 0.07142857142857142,
                "lgd": 0.5714285714285714,
                "meta": {
                    "use_camera": False,
                    "use_lidar": False,
                    "use_radar": False,
                    "use_map": False,
                    "use_external": True,
                },
            },
            "results_02": {
                "label_metrics": {
                    "amota": {"car": 0.7094932191291934},
                    "amotp": {"car": 1.0094938375648046},
                    "recall": {"car": 0.9162910495814552},
                    "motar": {"car": 0.8108493932905068},
                    "gt": {"car": 1553.0},
                    "mota": {"car": 0.7314874436574372},
                    "motp": {"car": 0.8679929572169196},
                    "mt": {"car": 14.0},
                    "ml": {"car": 1.0},
                    "faf": {"car": 252.38095238095238},
                    "tp": {"car": 1401.0},
                    "fp": {"car": 265.0},
                    "fn": {"car": 130.0},
                    "ids": {"car": 22.0},
                    "frag": {"car": 10.0},
                    "tid": {"car": 0.07142857142857142},
                    "lgd": {"car": 0.6428571428571429},
                },
                "eval_time": SKIP_TEST_HINT,
                "cfg": {
                    "tracking_names": ["car"],
                    "pretty_tracking_names": {"car": "Car"},
                    "tracking_colors": {"car": "C0"},
                    "class_range": {"car": 1000000.0},
                    "dist_fcn": "center_distance",
                    "dist_th_tp": 2.0,
                    "min_recall": 0.1,
                    "max_boxes_per_sample": 500,
                    "metric_worst": {
                        "amota": 0.0,
                        "amotp": 2.0,
                        "recall": 0.0,
                        "motar": 0.0,
                        "mota": 0.0,
                        "motp": 2.0,
                        "mt": 0.0,
                        "ml": -1.0,
                        "faf": 500,
                        "gt": -1,
                        "tp": 0.0,
                        "fp": -1.0,
                        "fn": -1.0,
                        "ids": -1.0,
                        "frag": -1.0,
                        "tid": 20,
                        "lgd": 20,
                    },
                    "num_thresholds": 40,
                },
                "amota": 0.7094932191291934,
                "amotp": 1.0094938375648046,
                "recall": 0.9162910495814552,
                "motar": 0.8108493932905068,
                "gt": 1553.0,
                "mota": 0.7314874436574372,
                "motp": 0.8679929572169196,
                "mt": 14.0,
                "ml": 1.0,
                "faf": 252.38095238095238,
                "tp": 1401.0,
                "fp": 265.0,
                "fn": 130.0,
                "ids": 22.0,
                "frag": 10.0,
                "tid": 0.07142857142857142,
                "lgd": 0.6428571428571429,
                "meta": {
                    "use_camera": False,
                    "use_lidar": False,
                    "use_radar": False,
                    "use_map": False,
                    "use_external": True,
                },
            },
            "all": {
                "label_metrics": {
                    "amota": {"car": 0.6997505345687811},
                    "amotp": {"car": 1.0117562380856717},
                    "recall": {"car": 0.9179008370895042},
                    "motar": {"car": 0.7997148966500356},
                    "gt": {"car": 3106.0},
                    "mota": {"car": 0.7224726336123632},
                    "motp": {"car": 0.8705785578121964},
                    "mt": {"car": 28.0},
                    "ml": {"car": 2.0},
                    "faf": {"car": 267.6190476190476},
                    "tp": {"car": 2806.0},
                    "fp": {"car": 562.0},
                    "fn": {"car": 255.0},
                    "ids": {"car": 45.0},
                    "frag": {"car": 18.0},
                    "tid": {"car": 0.07142857142857142},
                    "lgd": {"car": 0.6071428571428571},
                },
                "eval_time": SKIP_TEST_HINT,
                "cfg": {
                    "tracking_names": ["car"],
                    "pretty_tracking_names": {"car": "Car"},
                    "tracking_colors": {"car": "C0"},
                    "class_range": {"car": 1000000.0},
                    "dist_fcn": "center_distance",
                    "dist_th_tp": 2.0,
                    "min_recall": 0.1,
                    "max_boxes_per_sample": 500,
                    "metric_worst": {
                        "amota": 0.0,
                        "amotp": 2.0,
                        "recall": 0.0,
                        "motar": 0.0,
                        "mota": 0.0,
                        "motp": 2.0,
                        "mt": 0.0,
                        "ml": -1.0,
                        "faf": 500,
                        "gt": -1,
                        "tp": 0.0,
                        "fp": -1.0,
                        "fn": -1.0,
                        "ids": -1.0,
                        "frag": -1.0,
                        "tid": 20,
                        "lgd": 20,
                    },
                    "num_thresholds": 40,
                },
                "amota": 0.6997505345687811,
                "amotp": 1.0117562380856717,
                "recall": 0.9179008370895042,
                "motar": 0.7997148966500356,
                "gt": 3106.0,
                "mota": 0.7224726336123632,
                "motp": 0.8705785578121964,
                "mt": 28.0,
                "ml": 2.0,
                "faf": 267.6190476190476,
                "tp": 2806.0,
                "fp": 562.0,
                "fn": 255.0,
                "ids": 45.0,
                "frag": 18.0,
                "tid": 0.07142857142857142,
                "lgd": 0.6071428571428571,
                "meta": {
                    "use_camera": False,
                    "use_lidar": False,
                    "use_radar": False,
                    "use_map": False,
                    "use_external": True,
                },
            },
        }
    }


def test_convert_and_evaluate_pass() -> None:
    # Prepare test data and config
    example_data_dir: str = obtain_test_cases()

    config = CustomDataEvalConfig(
        data_root=example_data_dir,
        force_regenerate=True,
        subdir_pattern="sim15data",
        nuscenes_eval_config_path="inputs/artery/to_nuscenes/artery_config_for_nuscenes.json",
    )

    # Function under test
    actual_metrics = convert_and_evaluate(config)

    # Assertions
    assert isinstance(actual_metrics, dict)
    metrics_output_dir = os.path.join(example_data_dir, "nuscenes/sim15data/tracking_metrics")
    assert os.path.isdir(os.path.join(metrics_output_dir, "all"))
    assert os.path.isdir(os.path.join(metrics_output_dir, "results_01"))
    assert os.path.isdir(os.path.join(metrics_output_dir, "results_02"))

    expected_metrics: dict = get_expected_metrics_on_example_data()
    assert_equal(actual=actual_metrics, expected=expected_metrics)


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
