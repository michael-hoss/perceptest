py_library(
    name = "nuscenes_format",
    srcs = ["nuscenes_format.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//base/geometry",
    ],
)

py_test(
    name = "nuscenes_format_test",
    srcs = ["nuscenes_format_test.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":nuscenes_format",
        "//:conftest",
    ],
)

py_binary(
    name = "evaluate_tracking",
    srcs = ["evaluate_tracking.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//inputs/nuscenes:nuscenes_format",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking:evaluate",
    ],
)

py_test(
    name = "evaluate_tracking_unit_test",
    srcs = ["evaluate_tracking_unit_test.py"],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":evaluate_tracking",
        ":nuscenes_format",
        "//:conftest",
    ],
)

py_test(
    name = "evaluate_tracking_baseline_data_test",
    size = "enormous",
    srcs = ["evaluate_tracking_baseline_data_test.py"],
    data = [
        "//inputs/nuscenes:official_config_stripped.json",
    ],
    tags = [
        "local_only",
        "manual",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":evaluate_tracking",
        ":nuscenes_format",
        "//:conftest",
    ],
)

py_library(
    name = "data_insights",
    srcs = ["data_insights.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":nuscenes_format",
    ],
)
