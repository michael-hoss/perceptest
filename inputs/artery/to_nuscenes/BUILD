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
        "//inputs/nuscenes:nuscenes_format",
    ],
)

py_test(
    name = "to_nuscenes_test",
    srcs = [
        "to_nuscenes_test.py",
    ],
    tags = [
        "local_only",
    ],
    deps = [
        "//:conftest",
        "//inputs/artery:conftest",
        "//inputs/artery/to_nuscenes",
        "//inputs/nuscenes:data_insights",
    ],
)
