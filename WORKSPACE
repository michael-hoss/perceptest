workspace(name = "perceptest")

local_repository(
    name = "nuscenes-devkit",
    path = "third_party/nuscenes-devkit",
)

# Now, I can specify @nuscenes-devkit//python-sdk/nuscenes:nuscenes or others as a target here in the mother repo

# Note that in py_test, I also need to specify the PYTHONPATH according to how the nuscenes devkit expects it.
# This works with the imports attribute in py_test, which expects a path relative to the BUILD file.
# We need to navigate not to the `third_party` dir in the dir tree, but to the `nuscenes-devkit` dir that is
# a *sibling* of the `perceptest` dir in the bazel runfiles.
