py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    deps = [
        ":v2x_eval_lib",
        "//:conftest",
    ],
)

py_library(
    name = "v2x_eval_lib",
    srcs = [
        "constants.py",
        "convert_to_nuscenes.py",
        "obtain_tracking_metrics.py",
        "parse_cli.py",
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    deps = [
        "//:conftest",
        "//base/cli:suppress_stdout",
        "//inputs/artery:artery_lib",
        "//inputs/artery:conftest",
        "//inputs/artery/to_nuscenes",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:evaluate_tracking",
    ],
)
