py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    env = {
        "NUSCENES": "/data/sets/nuscenes",
    },
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
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    deps = [
        "//:conftest",
        "//inputs/artery:artery_lib",
        "//inputs/artery:conftest",
        "//inputs/artery/to_nuscenes",
        "//inputs/nuscenes:evaluate_tracking",
    ],
)
