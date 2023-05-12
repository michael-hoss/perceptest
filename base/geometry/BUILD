py_library(
    name = "geometry",
    srcs = [
        "aa_bounding_box.py",
        "vectors.py",
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "vectors_test",
    srcs = [
        "vectors_test.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":geometry",
        "//:conftest",
    ],
)
