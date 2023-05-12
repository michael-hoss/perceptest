py_library(
    name = "geo_coordinates",
    srcs = ["geo_coordinates.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "geo_coordinates_test",
    srcs = ["geo_coordinates_test.py"],
    deps = [
        ":geo_coordinates",
        "//:conftest",
    ],
)
