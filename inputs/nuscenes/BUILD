py_test(
    name = "evaluate_tracking_baseline_data_test",
    size = "enormous",
    srcs = ["evaluate_tracking_baseline_data_test.py"],
    data = [
        "//inputs/nuscenes:example_custom_config.json",
        "//inputs/nuscenes:official_config_stripped.json",
    ],
    imports = ["../../third_party/nuscenes-devkit/python-sdk"],  # add this to PYTHONPATH, relative to this BUILD file
    tags = [
        # it requires the downloaded nuscenes dataset, and downloaded baseline submissions, and takes too long
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
