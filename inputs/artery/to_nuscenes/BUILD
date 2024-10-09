exports_files(["artery_config_for_nuscenes.json"])

py_library(
    name = "to_nuscenes",
    srcs = [
        "to_nuscenes.py",
        "to_nuscenes_constants.py",
    ],
    visibility = [
        "//research:__subpackages__",
    ],
    deps = [
        "//inputs/artery:artery_lib",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:nuscenes_format",
    ],
)

py_test(
    name = "to_nuscenes_test",
    srcs = [
        "to_nuscenes_test.py",
    ],
    imports = ["../../../../nuscenes-devkit/python-sdk"],  # add this to PYTHONPATH, relative to this BUILD file
    tags = [
        "local_only",
    ],
    deps = [
        "//:conftest",
        "//inputs/artery:conftest",
        "//inputs/artery/to_nuscenes",
        "//inputs/nuscenes:data_insights",
        "@nuscenes-devkit//python-sdk/nuscenes/eval/tracking/tooling:nuscenes_format",
    ],
)
