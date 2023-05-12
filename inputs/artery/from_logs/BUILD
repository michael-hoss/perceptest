py_library(
    name = "from_logs",
    srcs = [
        "main_loader.py",
        "raw_parsing.py",
        "timestamps.py",
        "transform_coordinates.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//base/geo_coordinates",
        "//inputs/artery:artery_format",
    ],
)

py_test(
    name = "timestamps_test",
    srcs = [
        "timestamps_test.py",
    ],
    deps = [
        ":from_logs",
        "//:conftest",
    ],
)

py_test(
    name = "main_loader_test",
    srcs = [
        "main_loader_test.py",
    ],
    tags = [
        "local_only",
    ],
    deps = [
        ":from_logs",
        "//:conftest",
        "//inputs/artery:conftest",
    ],
)

py_test(
    name = "transform_coordinates_test",
    srcs = [
        "transform_coordinates_test.py",
    ],
    tags = [
        "local_only",
    ],
    deps = [
        ":from_logs",
        "//:conftest",
        "//base/geometry",
        "//inputs/artery:conftest",
    ],
)

py_test(
    name = "raw_parsing_test",
    srcs = [
        "raw_parsing_test.py",
    ],
    tags = [
        "local_only",
    ],
    deps = [
        "//:conftest",
        "//inputs/artery:artery_lib",
        "//inputs/artery:conftest",
    ],
)

py_binary(
    name = "main_loader_analysis",
    srcs = [
        "main_loader_analysis.py",
    ],
    deps = [
        "//:conftest",
        "//inputs/artery:artery_lib",
        "//inputs/artery:conftest",
    ],
)
