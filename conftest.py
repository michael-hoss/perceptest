from os import environ

import debugpy
import pytest


def use_debugpy():
    """Also define this as a non-fixture function to use it in files that are not pytest tests."""

    # See also https://code.visualstudio.com/docs/python/debugging
    # To set this env var in bazel test, use --test_env=DEBUG=1
    if environ.get("DEBUG") == "1":
        # Make sure the IDE's debugger attaches to this port
        debugpy.listen(("localhost", 5678))
        print("Waiting for debugger to attach...")
        debugpy.wait_for_client()
        print("Debugger attached. Starting execution.")


@pytest.fixture(scope="session", autouse=True)
def use_debugpy_in_pytests():
    use_debugpy()
