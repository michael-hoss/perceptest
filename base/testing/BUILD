py_library(
    name = "assertions",
    srcs = [
        "recursive_assert_equal.py",
    ],
)

py_test(
    name = "recursive_assert_equal_test",
    srcs = [
        "recursive_assert_equal_test.py",
    ],
    deps = [
        ":assertions",
        "//:conftest",
    ],
)
