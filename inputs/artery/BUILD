py_library(
    name = "artery_lib",
    srcs = [],
    visibility = ["//visibility:public"],
    deps = [
        ":artery_format",
        "//inputs/artery/from_logs",
    ],
)

py_library(
    name = "artery_format",
    srcs = [
        "artery_format.py",
    ],
    visibility = ["//visibility:public"],
)

py_library(
    name = "conftest",
    srcs = [
        "conftest.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":artery_lib",
        ":obtain_test_data",
    ],
)

py_binary(
    name = "obtain_test_data",
    srcs = [
        "obtain_test_data.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//base/file_utils",
    ],
)
