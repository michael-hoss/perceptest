py_binary(
    name = "main",
    srcs = [
        "main.py",
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    deps = [
        ":artery_convert_lib",
        "//:conftest",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:custom_data_eval_lib",
    ],
)

py_library(
    name = "artery_convert_lib",
    srcs = [
        "convert_to_nuscenes.py",
    ],
    deps = [
        "//:conftest",
        "//base/cli:suppress_stdout",
        "//inputs/artery:artery_lib",
        "//inputs/artery:conftest",
        "//inputs/artery/to_nuscenes",
    ],
)

py_test(
    name = "main_test",
    size = "medium",
    srcs = [
        "main_test.py",
    ],
    data = [
        "//inputs/artery/to_nuscenes:artery_config_for_nuscenes.json",
    ],
    tags = [
        "requires_download",
    ],
    deps = [
        ":main",
        "//:conftest",
        "//base/testing:assertions",
    ],
)
