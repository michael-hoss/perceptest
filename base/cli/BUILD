py_library(
    name = "suppress_stdout",
    srcs = ["suppress_stdout.py"],
    visibility = ["//visibility:public"],
    deps = [],
)

py_test(
    name = "suppress_stdout_test",
    srcs = ["suppress_stdout_test.py"],
    deps = [
        ":suppress_stdout",
        "//:conftest",
    ],
)
