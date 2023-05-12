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
    ],
)
