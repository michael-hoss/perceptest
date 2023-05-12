py_binary(
    name = "eval_artery_on_nuscenes",
    srcs = [
        "eval_artery_on_nuscenes.py",
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
