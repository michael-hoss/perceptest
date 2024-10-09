py_test(
    name = "evaluate_tracking_baseline_data_test",
    size = "enormous",
    srcs = ["evaluate_tracking_baseline_data_test.py"],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
        "//inputs/nuscenes:official_config_stripped.json",
    ],
    tags = [
        "local_only",
        "manual",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//:conftest",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:evaluate_tracking",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:nuscenes_format",
    ],
)

py_library(
    name = "data_insights",
    srcs = ["data_insights.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:nuscenes_format",
    ],
)
